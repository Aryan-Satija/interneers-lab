from rest_framework.test import APITestCase
from django.urls import reverse
from mongoengine import connect, disconnect
from product.models import Category
import random, string

class CategoryAPITestCase(APITestCase):
    
    @classmethod
    def setUpClass(productTestCaseClass):
        super().setUpClass()
        connect("inventory", alias="inventory", host="mongodb://root:example@localhost:27018/inventory?authSource=admin")
        
    @classmethod
    def tearDownClass(productTestCaseClass):
        disconnect(alias="inventory")
        super().tearDownClass()
    
    def test_add_category_valid(self):
        url = reverse("category-add") 

        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

        payload = {
            "name": random_name,
            "description": "A test category"
        }

        original_count = Category.objects.count()

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), original_count + 1)

    def test_add_category_missing_name(self):
        url = reverse("category-add")

        payload = {
            "description": "A test category"
        }

        original_count = Category.objects.count()

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Category.objects.count(), original_count)