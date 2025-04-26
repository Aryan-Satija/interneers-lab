from rest_framework.test import APITestCase
from django.urls import reverse
from mongoengine import connect, disconnect
from product.seed_db import run_seed
from product.repository import ProductRepository, CategoryRepository, BrandRepository, ProductNotFound, ProductValidationError
from parameterized import parameterized

product_repository = ProductRepository()
category_repository = CategoryRepository()
brand_repository = BrandRepository()

class ProductAPITestCase(APITestCase):
    
    @classmethod
    def setUpClass(productTestCaseClass):
        super().setUpClass()
        
        connect("inventory", alias="inventory", host="mongodb://root:example@localhost:27018/inventory?authSource=admin")
        
        run_seed()
        
        productTestCaseClass.test_brand = brand_repository.create_brand({'name':"Test Brand", 'description':"Test Description"})
        productTestCaseClass.test_category = category_repository.create_category({'name': "Test Ctegory", 'description': "Test Description"})
        productTestCaseClass.test_product = product_repository.create_product({'name':"Test Product", 'description':"Test Description", 'quantity':10, 'price':100000, 'brand':str(productTestCaseClass.test_brand.id), 'category':str(productTestCaseClass.test_category.id)})
        

    @classmethod
    def tearDownClass(productTestCaseClass):
        
        brand_repository.delete_brand(productTestCaseClass.test_brand.id)
        category_repository.delete_category(productTestCaseClass.test_category.id)
        product_repository.delete_product(productTestCaseClass.test_product)

        super().tearDownClass()
    
    def test_get_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url, {'page': 1, 'page_size': 5})
        self.assertEqual(response.status_code, 200)
    
    @parameterized.expand([ (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,) ])
    def test_get_product_list_within_limit(self, page_size):
        url = reverse('product-list')
        response = self.client.get(url, {'page': 1, 'page_size': page_size})
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data['products']), page_size)
    
    def test_pagination_beyond_available_pages(self):
        url = reverse('product-list')
        response = self.client.get(url, {'page': 9999, 'page_size': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['products']), 0)
    
    def test_get_product_list_filter_by_price(self):
        
        url, min_price, max_price = "/api/v1/product/", 50000, 70000
        response = self.client.get(url, {'min_price': min_price, 'max_price': max_price})
        
        prices = [pp['price'] for pp in response.data['products']]
        
        for price in prices:
            self.assertLessEqual(price, max_price)
            self.assertGreaterEqual(price, min_price)
            
    def test_get_product_list_filter_by_name(self):
        
        url, name = reverse('product-list'), "dell"
        response = self.client.get(url, {'name': name})
        
        names = [pp['name'] for pp in response.data['products']]
        
        self.assertTrue(all(name in nm for nm in names))
    
    def test_get_product_list_combined_filters(self):
        
        url = reverse('product-list')
        filters = {'name': self.test_product.name, 'min_price': 10000, 'max_price': 50000, 'page': 1, 'page_size': 5}
        response = self.client.get(url, filters)
        
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data['products']), filters['page_size'])
        
        for product in response.data['products']:
            self.assertEqual(product.name, filters['name'])
            self.assertGreaterEqual(product.price, filters['min_price'])
            self.assertLessEqual(product.price, filters['max_price'])
        
        
    def test_create_product_valid(self):
        url = reverse('product-list')
        response = self.client.post(url, { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": 5, "category": str(self.test_category.id), "brand": str(self.test_brand.id) }, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_product_missing_product_details(self):
        url = reverse('product-list')
        
        bad_products = [
            { "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": 5, "category": str(self.test_category.id), "brand": str(self.test_brand.id) }, # no name
            { "name": "Apple MacBook Air", "price": 100000, "quantity": 5, "category": str(self.test_category.id), "brand": str(self.test_brand.id) }, # no description
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "quantity": 5, "category": str(self.test_category.id), "brand": str(self.test_brand.id) }, # no price
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "category": str(self.test_category.id), "brand": str(self.test_brand.id) }, # no quantity
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": 5, "brand": str(self.test_brand.id) }, # no category
        ]
        
        for bad_product in bad_products:
            response = self.client.post(url, bad_product, format="json")
            self.assertEqual(response.status_code, 400)

    def test_create_product_invalid_product_details(self):
        url = reverse('product-list')
        
        bad_products = [
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": -100000, "quantity": 5, "category": str(self.test_category.id), "brand": str(self.test_brand.id) }, # negative price
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": -5, "category": str(self.test_category.id), "brand": str(self.test_brand.id) }, # negative quantity
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": 5, "category": "67e8ef6bd739b2427101bddc", "brand": str(self.test_brand.id) }, # non-existent category
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": 5, "category": str(self.test_category.id), "brand": "67dc2fb0fead7871ab74c197" }, # non-existent brand
        ]
        
        for bad_product in bad_products:
            response = self.client.post(url, bad_product, format="json")
            self.assertEqual(response.status_code, 400)
    
    def test_get_product_details_valid(self):
        url = reverse('product-list')
        url = url + str(self.test_product.id) + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_product_details_invalid(self):
        invalid_id = "605c5c5d8f1b2c1e1e1e1e1e"
        url = reverse('product-list')
        url = url + invalid_id + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_put_product_valid(self):
        url = reverse('product-list')
        url = url + str(self.test_product.id) + "/"
        data = {"name": self.test_product.name, "description": self.test_product.description, "price": self.test_product.price, "quantity": self.test_product.quantity, "category": str(self.test_category.id), "brand": str(self.test_brand.id)}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_put_product_not_found(self):
        invalid_id = "605c5c5d8f1b2c1e1e1e1e1e"
        url = reverse('product-list')
        url = url + invalid_id + "/"
        data = {"name": self.test_product.name, "description": self.test_product.description, "price": self.test_product.price, "quantity": self.test_product.quantity, "category": str(self.test_category.id), "brand": str(self.test_brand.id)}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_product_valid(self):
        temp_product = product_repository.create_product(
            {                
                'name':"Temporary Product",
                'description':"Temporary Product Description",
                'quantity':10,
                'price':50000,
                'brand':str(self.test_brand.id),
                'category':str(self.test_category.id)
            }
        )
        
        url = reverse('product-list') + f"{temp_product.id}/"
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(ProductNotFound):
            product_repository.get_product_by_id(temp_product.id)

    def test_delete_product_invalid(self):
        invalid_id = "605c5c5d8f1b2c1e1e1e1e1e"
        url = reverse('product-list') + f"{invalid_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
    
    