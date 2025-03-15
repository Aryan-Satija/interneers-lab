import datetime

from mongoengine import StringField, DateTimeField, FloatField, IntField, ReferenceField, CASCADE, Document

class Category(Document):
    
    name = StringField(required=True, unique=True, max_length=100)
    description = StringField(required=True)
    
    def __str__(self):
        return self.name
    
class Brand(Document):
    
    name = StringField(required=True, unique=True, max_length=100)
    description = StringField(required=True)

    def __str__(self):
        return self.name

class Products(Document):
    
    name = StringField(required=True, max_length=100)
    description = StringField(required=True)
    price = FloatField(required=True, default=0)
    quantity = IntField(required=True, default=0)
    brand = ReferenceField(Brand, required=True, reverse_delete_rule=CASCADE)
    category = ReferenceField(Category, required=True, reverse_delete_rule=CASCADE)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name