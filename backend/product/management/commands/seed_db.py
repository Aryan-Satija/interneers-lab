import os
from django.core.management.base import BaseCommand
from product.services.category_service import CategoryService
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

USE_LOCAL_DB = os.getenv("USE_LOCAL_DB", False) == "true"

category_service = CategoryService()

fake = Faker()
fake.seed_instance(11)


class Command(BaseCommand):  
    help = "Seeds the database"

    def handle(self, *args, **kwargs):
        if not USE_LOCAL_DB:
            self.stdout.write(self.style.ERROR("CAN'T SEED CLOUD DB"))
            return
        
        for i in range(10):
            name = fake.name()
            description = fake.sentence(nb_words=10)
            data, error = category_service.create_category({"name": name, "description": description})
            if error:
                self.stdout.write(self.style.ERROR(f"Error creating category {name}: {error}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Category {name} created successfully"))
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))