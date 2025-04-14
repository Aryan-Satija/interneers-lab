from ..repository import productRepository
from ..serializers import ProductsSerializer

class ProductService:
    
    def __init__(self):
        self.product_repository = productRepository()
        
    def get_paginated_products(self, page, page_size, get_product_request, sort_by = '-created_at'):
        if page < 1 or page_size < 1:
            return None, {"error": "Invalid pagination values"}
        
        start = (page - 1) * page_size
        end = start + page_size
        products = self.product_repository.get_all_products(start, end, get_product_request, sort_by)
        return ProductsSerializer(products, many = True).data
    
    def get_product_by_id(self, product_id):
        product = self.product_repository.get_product_by_id(product_id)
        
        if not product:
            return None
        
        return ProductsSerializer(product).data
    
    def create_product(self, data):
        required_fields = ["name", "description", "price", "quantity", "category", "brand"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return None, {"error": f"Missing required fields: {', '.join(missing_fields)}"}
        
        if data.get("price") < 0:
            return None, {"error": "Price cannot be negative"}
        
        if data.get("quantity") < 0:
            return None, {"error": "Quantity cannot be negative"}
        
        serializer = ProductsSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data, None
        
        return None, serializer.errors   
    
    def update_product(self, product_id, data):
        required_fields = ["name", "description", "price", "quantity", "category", "brand"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return None, {"error": f"Missing required fields: {', '.join(missing_fields)}"}
        
        if data.get("price") < 0:
            return None, {"error": "Price cannot be negative"}
        
        if data.get("quantity") < 0:
            return None, {"error": "Quantity cannot be negative"}
        
        product = self.product_repository.get_product_by_id(product_id)
        
        if not product:
            return None, {"error": "Product does not exist"}

        serializer = ProductsSerializer(product, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data, None
        
        return None, serializer.errors

    def delete_product(self, product_id):
        product = self.product_repository.get_product_by_id(product_id)
        
        if not product:
            return {"error": "Product does not exist"}, True

        self.product_repository.delete_product(product)
        return {"message": "Product Deleted Successfully"}, False