from rest_framework.test import APITestCase
from django.urls import reverse
from mongoengine import connect, disconnect
from product.models import Products, Brand, Category
from product.seed_db import run_seed

class ProductAPITestCase(APITestCase):
    
    @classmethod
    def setUpClass(productTestCaseClass):
        super().setUpClass()
        
        connect("inventory", alias="inventory", host="mongodb://root:example@localhost:27018/inventory?authSource=admin")
        
        run_seed()
        
        productTestCaseClass.testbrand = Brand(name="Test Brand", description="Test Description").save()
        productTestCaseClass.testcategory = Category(name="Test Ctegory", description="Test Description").save()
        productTestCaseClass.testproduct = Products(name="Test Product", description="Test Description", quantity=10, price=100000, brand=productTestCaseClass.testbrand, category=productTestCaseClass.testcategory).save()
        
        

    @classmethod
    def tearDownClass(productTestCaseClass):
        Brand.objects(name="Test Brand").delete()
        Category.objects(name="Test Ctegory").delete()
        Products.objects(name="Test Product").delete()   
        
        disconnect(alias="inventory")
        super().tearDownClass()
    
    def test_get_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url, {'page': 1, 'page_size': 5})
        self.assertEqual(response.status_code, 200)
    
    def test_get_product_list_within_limit(self):
        url = reverse('product-list')
        page_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        for page_size in page_sizes:
            response = self.client.get(url, {'page': 1, 'page_size': page_size})
            self.assertLessEqual(len(response.data['products']), page_size)
    
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
    
    def test_create_product_valid(self):
        url = reverse('product-list')
        response = self.client.post(url, { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": 5, "category": "67e8ef6bd739b2427101bddc", "brand": "67dc2fb0fead7871ab74c197" }, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_product_missing_product_details(self):
        url = reverse('product-list')
        
        bad_products = [
            { "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": 5, "category": "67e8ef6bd739b2427101bddc", "brand": "67dc2fb0fead7871ab74c197" },
            { "name": "Apple MacBook Air", "price": 100000, "quantity": 5, "category": "67e8ef6bd739b2427101bddc", "brand": "67dc2fb0fead7871ab74c197" },
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "quantity": 5, "category": "67e8ef6bd739b2427101bddc", "brand": "67dc2fb0fead7871ab74c197" },
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "category": "67e8ef6bd739b2427101bddc", "brand": "67dc2fb0fead7871ab74c197" },
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": 5, "brand": "67dc2fb0fead7871ab74c197" },
        ]
        
        for bad_product in bad_products:
            response = self.client.post(url, bad_product, format="json")
            self.assertEqual(response.status_code, 400)

    def test_create_product_invalid_product_details(self):
        url = reverse('product-list')
        
        bad_products = [
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": -100000, "quantity": 5, "category": "67e8ef6bd739b2427101bddc", "brand": "67dc2fb0fead7871ab74c197" }, # negative price
            { "name": "Apple MacBook Air", "description": "Apple M4 chip with 10-core CPU", "price": 100000, "quantity": -5, "category": "67e8ef6bd739b2427101bddc", "brand": "67dc2fb0fead7871ab74c197" }, # negative quantity
        ]
        
        for bad_product in bad_products:
            response = self.client.post(url, bad_product, format="json")
            self.assertEqual(response.status_code, 400)
    
    def test_get_product_details_valid(self):
        url = reverse('product-list')
        url = url + str(self.testproduct.id) + "/"
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
        url = url + str(self.testproduct.id) + "/"
        data = {"name": self.testproduct.name, "description": self.testproduct.description, "price": self.testproduct.price, "quantity": self.testproduct.quantity, "category": str(self.testcategory.id), "brand": str(self.testbrand.id)}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_put_product_invalid(self):
        invalid_id = "605c5c5d8f1b2c1e1e1e1e1e"
        url = reverse('product-list')
        url = url + invalid_id + "/"
        data = {"name": self.testproduct.name, "description": self.testproduct.description, "price": self.testproduct.price, "quantity": self.testproduct.quantity, "category": str(self.testcategory.id), "brand": str(self.testbrand.id)}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)