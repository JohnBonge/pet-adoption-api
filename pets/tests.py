from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from userz.models import CustomUser
from .models import Pet

# Create your tests here.
class PetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="shelter1", password="pass", is_shelter=True)
        self.client.force_authenticate(user=self.user)

    def test_create_pet(self):
        url = reverse("pets-list")
        data = {"name":"Buddy","type":"Dog","breed":"Labrador","age":3,"available":True}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)