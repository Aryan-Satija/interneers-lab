from ..repository import ProductRepository
from ..exceptions import ProductNotFound, InvalidProductId, ProductValidationError
from ..serializers import ProductsSerializer

class ProductService:
    
    def __init__(self):
        self.product_repository = ProductRepository()
        
    def get_paginated_products(self, page, page_size, get_product_request, sort_by='-created_at'):
        if page < 1 or page_size < 1:
            raise ValueError('Invalid page or page size')
        
        start = (page - 1) * page_size
        end = start + page_size
        products = self.product_repository.get_all_products(start, end, get_product_request, sort_by)
        return ProductsSerializer(products, many=True).data
    
    def get_product_by_id(self, product_id):
        if product_id is None:
            raise InvalidProductId("Product ID must not be none")
        
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ProductNotFound(f"Product with id {product_id} not found")
        
        return ProductsSerializer(product).data
    
    def create_product(self, data):
        required_fields = self.product_repository.get_product_required_fields()
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        if data.get("price") < 0:
            raise ValueError("Price cannot be negative")
        
        if data.get("quantity") < 0:
            raise ValueError("Quantity cannot be negative")

        product = self.product_repository.create_product(data)
        if not product:
            raise ProductValidationError("Failed to create the product due to validation error.")
    
        return ProductsSerializer(product).data
    
    def update_product(self, product_id, data):
        required_fields = ["name", "description", "price", "quantity", "category", "brand"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        if data.get("price") < 0:
            raise ValueError("Price cannot be negative")
        
        if data.get("quantity") < 0:
            raise ValueError("Quantity cannot be negative")
        
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ProductNotFound(f"Product with id {product_id} not found")
        
        self.product_repository.update_product(product, data)

    def delete_product(self, product_id):
        if product_id is None:
            raise InvalidProductId("Product ID must not be none")
        
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ProductNotFound(f"Product with id {product_id} not found")
        
        self.product_repository.delete_product(product)
