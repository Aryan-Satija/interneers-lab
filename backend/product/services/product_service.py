from ..repository import productRepository
from ..serializers import ProductsSerializer

class ProductService:
    
    @staticmethod
    def get_paginated_products(page, page_size, sort_by = '-created_at'):
        start = (page - 1) * page_size
        end = start + page_size
        products = productRepository.get_all_products(start, end, sort_by)
        return ProductsSerializer(products, many = True).data
    
    @staticmethod
    def get_product_by_id(product_id):
        product = productRepository.get_product_by_id(product_id)
        
        if not product:
            return None
        
        return ProductsSerializer(product).data
    
    @staticmethod
    def create_product(data):
        serializer = ProductsSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data, None
        
        return None, serializer.errors   
    
    @staticmethod
    def update_product(product_id, data):
        product = productRepository.get_product_by_id(product_id)
        
        if not product:
            return None, {"error": "Product does not exist"}

        serializer = ProductsSerializer(product, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data, None
        
        return None, serializer.errors

    @staticmethod
    def delete_product(product_id):
        product = productRepository.get_product_by_id(product_id)
        
        if not product:
            return {"error": "Product does not exist"}

        productRepository.delete_product(product)
        return {"message": "Product Deleted Successfully"}