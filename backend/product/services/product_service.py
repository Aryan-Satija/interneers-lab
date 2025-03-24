from ..repository import productRepository
from ..serializers import ProductsSerializer

class ProductService:
    
    def __init__(self):
        self.product_repository = productRepository()
        
    def get_paginated_products(self, page, page_size, name, min_price, max_price, brand, category, sort_by = '-created_at'):
        start = (page - 1) * page_size
        end = start + page_size
        print(self, page, page_size, name, min_price, max_price, brand, category, sort_by)
        products = self.product_repository.get_all_products(start, end, name, min_price, max_price, brand, category, sort_by)
        return ProductsSerializer(products, many = True).data
    
    def get_product_by_id(self, product_id):
        product = self.product_repository.get_product_by_id(product_id)
        
        if not product:
            return None
        
        return ProductsSerializer(product).data
    
    def create_product(self, data):
        serializer = ProductsSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data, None
        
        return None, serializer.errors   
    
    def update_product(self, product_id, data):
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
            return {"error": "Product does not exist"}

        self.product_repository.delete_product(product)
        return {"message": "Product Deleted Successfully"}