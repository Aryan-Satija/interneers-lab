from .models import Products, Category, Brand
from mongoengine.queryset.visitor import Q
from mongoengine import ValidationError 
from .exceptions import BrandNotFound, BrandValidationError, CategoryNotFound, CategoryValidationError, ProductNotFound, ProductValidationError, InvalidProductId
from mongoengine import ReferenceField

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
            
        return Products.objects.filter(query).order_by(sort_by)[start:end], Products.objects.count()
    
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
        
    def update_product(self, product_id, data):
        if product_id is None or data is None:
            raise ValueError("Product ID and update data must not be none")
        
        excluded_fields = {'id', '_id'}
        
        reference_fields = {
            field: field_obj for field, field_obj in Products._fields.items() 
            if isinstance(field_obj, ReferenceField)
        }

        other_fields = {
            field: field_obj for field, field_obj in Products._fields.items()
            if field not in reference_fields
            and field not in excluded_fields
        }

        update_data = {}
    
        for field, field_obj in reference_fields.items():
            if field in data:
                try:
                    ref_model = field_obj.document_type
                    ref_doc = ref_model.objects.get(id=data[field])
                    update_data[f"set__{field}"] = ref_doc
                except ref_model.DoesNotExist:
                    raise ProductValidationError(f"Invalid reference for '{field}'")
                except Exception:
                    raise ProductValidationError(f"Invalid ID format for '{field}'")

        for field in other_fields:
            if field in data:
                update_data[f"set__{field}"] = data[field]
                  
        try:
            Products.objects(id=product_id).update(**update_data)            
            return Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            raise ProductNotFound(product_id)
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

    def get_all_categories(self):
        return Category.objects.all()
        
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
        
    def get_all_brands(self):
        return Brand.objects.all()