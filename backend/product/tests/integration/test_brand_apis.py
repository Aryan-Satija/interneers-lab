from rest_framework.test import APITestCase
from django.urls import reverse
from mongoengine import connect, disconnect
from product.models import Brand
import random, string
class BrandAPITestCase(APITestCase):
    
    @classmethod
    def setUpClass(productTestCaseClass):
        super().setUpClass()
        connect("inventory", alias="inventory", host="mongodb://root:example@localhost:27018/inventory?authSource=admin")

    @classmethod
    def tearDownClass(productTestCaseClass): 
        disconnect(alias="inventory")
        super().tearDownClass()
        
    def test_add_brand_valid(self):
        url = reverse("brand-add") 
        
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=25))
        
        payload = {
            "name": random_name,
            "description": "A sample brand for testing"
        }

        original = Brand.objects.count()
        
        response = self.client.post(url, payload, format="json")
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Brand.objects.count(), original + 1)

    def test_add_brand_missing_name(self):
        url = reverse("brand-add")
        
        payload = {
            "description": "A sample brand for testing"
        }

        original = Brand.objects.count()
        
        response = self.client.post(url, payload, format="json")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Brand.objects.count(), original)
        