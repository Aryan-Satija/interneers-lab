import unittest
from unittest.mock import patch
from product.services.product_service import ProductService
from product.services.category_service import CategoryService


class TestProductService(unittest.TestCase):
    
    @patch('product.services.product_service.productRepository')
    def setUp(self, mockProductRepository):
        self.product_service = ProductService()
        self.product_service.product_repository = mockProductRepository()
    
    @patch('product.services.product_service.ProductsSerializer')
    def test_get_paginated_products_invalid(self, mockSerializer):
        self.product_service.product_repository.get_all_products.return_value = []
        mockSerializer.return_value.data = []
        data, error = self.product_service.get_paginated_products(-1, -1, {'max_price': 1200}, 'name')
        self.assertIsNone(data)

    @patch('product.services.product_service.ProductsSerializer')
    def test_get_paginated_products_valid(self, mockSerializer):
        self.product_service.product_repository.get_all_products.return_value = []
        mockSerializer.return_value.data = []
        data = self.product_service.get_paginated_products(1, 5, {'max_price': 1200}, 'name')
        self.assertIsInstance(data, list)
    
    @patch('product.services.product_service.ProductsSerializer')
    def test_create_product_missing_fields(self, mockSerializer):
        mockSerializer.return_value.is_valid = lambda: True
        mockSerializer.return_value.data = [] 
        
        incomplete_products = [
            {
                "description": "Gaming Laptop",
                "price": 1200,
                "quantity": 5,
                "category": "67e8ef6bd739b2427101bddc",
                "brand": "67dc2fb0fead7871ab74c197"
            },
            {
                "name": "Laptop",
                "description": "Gaming Laptop",
                "quantity": 5,
                "category": "67e8ef6bd739b2427101bddc",
                "brand": "67dc2fb0fead7871ab74c197"
            },
            {
                "name": "Laptop",
                "description": "Gaming Laptop",
                "price": 1200,
                "quantity": 5,
                "brand": "67dc2fb0fead7871ab74c197"
            },
            {
                "name": "Laptop",
                "description": "Gaming Laptop",
                "price": 1200,
                "category": "67e8ef6bd739b2427101bddc",
                "brand": "67dc2fb0fead7871ab74c197"
            },
            {
                "name": "Laptop",
                "description": "Gaming Laptop",
                "price": 1200,
                "category": "67e8ef6bd739b2427101bddc",
            }
        ]
        
        for incomplete_product in incomplete_products:
            data, errors = self.product_service.create_product(incomplete_product)
            self.assertIsNone(data)
            self.assertIsNotNone(errors)
    
    @patch('product.services.product_service.ProductsSerializer')
    def test_create_product_negative_price(self, mockSerializer):
        mockSerializer.return_value.is_valid = lambda: True
        mockSerializer.return_value.data = [] 
        
        product = {
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": -1200,
            "quantity": 5,
            "category": "67e8ef6bd739b2427101bddc",
            "brand": "67dc2fb0fead7871ab74c197"
        }
        
        data, errors = self.product_service.create_product(product)
        
        self.assertIsNone(data)
        self.assertEqual(errors, {"error": "Price cannot be negative"})
    
    @patch('product.services.product_service.ProductsSerializer')
    def test_create_product_negative_quantity(self, mockSerializer):
        mockSerializer.return_value.is_valid = lambda: True
        mockSerializer.return_value.data = [] 
        
        product = {
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": 1200,
            "quantity": -5,
            "category": "67e8ef6bd739b2427101bddc",
            "brand": "67dc2fb0fead7871ab74c197"
        }
        
        data, errors = self.product_service.create_product(product)
        
        self.assertIsNone(data)
        self.assertEqual(errors, {"error": "Quantity cannot be negative"})
        
    @patch('product.services.product_service.ProductsSerializer')
    def test_update_product_negative_price(self, mockSerializer):
        mockSerializer.return_value.is_valid = lambda: True
        mockSerializer.return_value.data = [] 
        
        product_id = "67e8ef6bd739b2427101bddc"
        product = {
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": -1200,
            "quantity": 5,
            "category": "67e8ef6bd739b2427101bddc",
            "brand": "67dc2fb0fead7871ab74c197"
        }
        
        data, errors = self.product_service.update_product(product_id, product)
        
        self.assertIsNone(data)
        self.assertEqual(errors, {"error": "Price cannot be negative"})
    
    @patch('product.services.product_service.ProductsSerializer')
    def test_update_product_negative_quantity(self, mockSerializer):
        mockSerializer.return_value.is_valid = lambda: True
        mockSerializer.return_value.data = [] 
        
        product_id = "67e8ef6bd739b2427101bddc"
        product = {
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": 1200,
            "quantity": -5,
            "category": "67e8ef6bd739b2427101bddc",
            "brand": "67dc2fb0fead7871ab74c197"
        }
        
        data, errors = self.product_service.update_product(product_id, product)
        
        self.assertIsNone(data)
        self.assertEqual(errors, {"error": "Quantity cannot be negative"})
    
    def test_get_product_not_found(self):
        self.product_service.product_repository.get_product_by_id.return_value = None
        
        product = {
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": 1200,
            "quantity": 5,
            "category": "67e8ef6bd739b2427101bddc",
            "brand": "67dc2fb0fead7871ab74c197"
        }
        
        result, error = self.product_service.update_product(1, product)
        
        self.assertIsNone(result)
        self.assertEqual(error, {"error": "Product does not exist"})

if __name__ == '__main__':
    unittest.main(verbosity=2)
