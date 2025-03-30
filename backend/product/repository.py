from .models import Products, Category, Brand
from mongoengine.queryset.visitor import Q

class productRepository:
    
    def get_all_products(self, start, end, get_product_request, sort_by = '-created_at'):
        allowed_sorts = ['name', '-name', 'price', '-price', 'created_at', '-created_at', 'updated_at', '-updated_at']
        
        if sort_by not in allowed_sorts:
            sort_by = '-created_at'
          
        query = Q()
          
        if get_product_request.name:
            query &= Q(name__icontains = get_product_request.name)
        if get_product_request.min_price:
            query &= Q(price__gte = get_product_request.min_price)
        if get_product_request.max_price:
            query &= Q(price__lte = get_product_request.max_price)
        if get_product_request.brand:
            brand_objs = Brand.objects.filter(name__in = get_product_request.brand)
            brand_ids = [brd.id for brd in brand_objs] 
            query &= Q(brand__in = brand_ids)
        if get_product_request.category:
            category_objs = Category.objects.filter(name__in=get_product_request.category)
            category_ids = [cat.id for cat in category_objs] 
            query &= Q(category__in=category_ids)  
            
        return Products.objects.filter(query).order_by(sort_by)[start:end]
    
    def get_product_by_id(self, product_id):
        return Products.objects.get(id = product_id)
    
    def create_product(self, product_data):
        return Products.objects.create(**product_data)
    
    def update_product(self, product, new_product):
        for item, val in new_product.items():
            setattr(product, item, val)
        product.save()
        return product
    
    def delete_product(self, product):
        product.delete()
