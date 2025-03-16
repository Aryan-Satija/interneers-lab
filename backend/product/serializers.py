from rest_framework_mongoengine.serializers import DocumentSerializer
import rest_framework.serializers as serializers
from .models import Products, Category, Brand
from bson import ObjectId

class ObjectIdField(serializers.Field):
    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except:
            raise serializers.ValidationError("Invalid ObjectId")        
    
    def to_representation(self, value):
        return str(value)
    
class BrandSerializer(DocumentSerializer):
    
    class Meta:
        model = Brand
        fields = '__all__'
        
class CategorySerializer(DocumentSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'

class ProductsSerializer(DocumentSerializer):
    
    brand = ObjectIdField()
    category = ObjectIdField()
    
    class Meta:
        model = Products
        fields = '__all__'