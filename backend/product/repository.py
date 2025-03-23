from .models import Products, Category, Brand
from mongoengine.queryset.visitor import Q

class productRepository:
    
    @staticmethod
    def get_all_products(start, end, name, min_price, max_price, brand, category, sort_by = '-created_at'):
        allowed_sorts = ['name', '-name', 'price', '-price', 'created_at', '-created_at', 'updated_at', '-updated_at']
        
        if sort_by not in allowed_sorts:
            sort_by = '-created_at'
          
        query = Q()
          
        if name:
            query &= Q(name__icontains = name)
        if min_price:
            query &= Q(price__gte = min_price)
        if max_price:
            query &= Q(price__lte = max_price)
        if brand:
            brand_obj = Brand.objects.filter(name__icontains = brand).first()
            if brand_obj:
                query &= Q(brand = brand_obj.id)
        if category:
            category_obj = Category.objects.filter(name__icontains = category).first()
            if category_obj:
                query &= Q(category = category_obj.id)
            
        return Products.objects.filter(query).order_by(sort_by)[start:end]
    
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
