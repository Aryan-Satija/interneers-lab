from .models import Products, Category, Brand

class productRepository:
    
    @staticmethod
    def get_all_products(start, end, sort_by = '-created_at'):
        allowed_sorts = ['name', '-name', 'price', '-price', 'created_at', '-created_at', 'updated_at', '-updated_at']
        
        if sort_by not in allowed_sorts:
            sort_by = '-created_at'
            
        return Products.objects.all().order_by(sort_by)[start:end]
    
    @staticmethod
    def get_product_by_id(product_id):
        return Products.objects.get(id = product_id)
    
    @staticmethod
    def create_product(product_data):
        return Products.objects.create(**product_data)
    
    @staticmethod
    def update_product(product, new_product):
        for item, val in new_product.items():
            setattr(product, item, val)
        product.save()
        return product
    
    @staticmethod
    def delete_product(product):
        product.delete()
