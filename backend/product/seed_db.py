# seed.py
import random
from faker import Faker
from mongoengine import connect

from product.models import Category, Brand, Products  

fake = Faker()

def seed_categories(n=5):
    
    categories = []
    
    for i in range(n):
        category = Category(name=fake.unique.word(), description=fake.sentence())
        category.save()
        categories.append(category)
    
    return categories

def seed_brands(n=5):
    
    brands = []
    
    for i in range(n):
        brand = Brand(name=fake.unique.word(), description=fake.catch_phrase())
        brand.save()
        brands.append(brand)
    
    return brands

def seed_products(n=20, brands = None, categories = None):
    
    if not brands:
        brands = seed_brands(n)
    
    if not categories:
        categories = seed_categories(n)
    
    brand_count, category_count = len(brands), len(categories)
    
    for i in range(n):
        product = Products(
            name=fake.unique.word().capitalize(),
            description=fake.sentence(nb_words=10),
            price=round(random.uniform(10, 1000), 2),
            quantity=random.randint(1, 100),
            brand=str(brands[i%brand_count].id),
            category=str(categories[i%category_count].id)
        )
        product.save()

def clear_all_collections():
    
    Category.drop_collection()
    Brand.drop_collection()
    Products.drop_collection()

def run_seed(cat_n=20, brand_n=20, prod_n=20):
    
    clear_all_collections()
    
    categories = seed_categories(cat_n)
    brands = seed_brands(brand_n)
    
    seed_products(prod_n, brands, categories)

