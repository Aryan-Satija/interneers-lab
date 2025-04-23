from .models import Products, Category, Brand
from mongoengine.queryset.visitor import Q
from mongoengine import ValidationError, DoesNotExist 
from .exceptions import BrandNotFound, BrandValidationError, CategoryNotFound, CategoryValidationError, ProductNotFound, ProductValidationError, InvalidProductId

class ProductRepository:
    
    def get_product_required_fields(self):
        return [field for field, field_obj in Products._fields.items() if field_obj.required]
            
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
        if product_id is None:
            raise InvalidProductId(product_id)
        
        try:
            return Products.objects.get(id = product_id)
        except Products.DoesNotExist:
            raise ProductNotFound(product_id)
        except ValidationError:
            raise InvalidProductId(product_id)
        
    def create_product(self, product_data):
        category_id, brand_id = product_data.get("category"), product_data.get("brand")
        
        if category_id is None or brand_id is None:
            raise ProductValidationError("Category and Brand are required")
        
        try:
            Brand.objects.get(id = brand_id)
            Category.objects.get(id = category_id)
        except Category.DoesNotExist:
            raise ProductValidationError("Invalid category ID")
        except Brand.DoesNotExist:
            raise ProductValidationError("Invalid brand ID")
        
        try:
            return Products.objects.create(**product_data)
        except ValidationError:
            raise ProductValidationError("Product data is invalid")
        
    def update_product(self, product, new_product):
        if product is None or new_product is None:
            raise ValueError("Product instance and update data must not be none")
        try:
            for item, val in new_product.items():
                if hasattr(product, item):
                    if item == "category":
                        category = Category.objects.get(id = val)
                        if not category:
                            raise ValueError("Category does not exist")
                        setattr(product, item, category)
                    elif item == "brand":
                        brand = Brand.objects.get(id = val)
                        if not brand:
                            raise ValueError("Brand does not exist")
                        setattr(product, item, brand)
                    else:
                        setattr(product, item, val)
                    
                else:
                    raise AttributeError(f"{item} is not a valid attribute")
            product.save()
            return product
        except ValidationError as e:
            raise ProductValidationError("Product validation failed")
    
    def delete_product(self, product):
        if product is None:
            raise ValueError("Product to be deleted must be passed in the arguments")
        
        try:
            product.delete()
        except Products.DoesNotExist:
            raise ProductNotFound(product.id)
        
class CategoryRepository:
    
    def create_category(self, data):
        try:
            return Category.objects.create(**data)
        except ValidationError:
            raise CategoryValidationError("Category validation failed")
        
    def delete_category(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
        except Category.DoesNotExist:
            raise CategoryNotFound(category_id)
        except ValidationError:
            raise CategoryValidationError("Invalid category ID")

        
class BrandRepository:
    
    def create_brand(self, data):
        try:
            return Brand.objects.create(**data)
        except ValidationError:
            raise BrandValidationError("Brand validation failed")
    
    def delete_brand(self, brand_id):
        try:
            brand = Brand.objects.get(id=brand_id)
            brand.delete()
        except Brand.DoesNotExist:
            raise BrandNotFound(brand_id)
        except ValidationError:
            raise BrandValidationError("Invalid brand ID")