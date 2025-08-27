from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
class UserTests(APITestCase):
    def test_register_login(self):
        url = reverse("register")
        data = {"username":"user1","email":"u@example.com","password":"pass123"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        login_url = reverse("login")
        login_resp = self.client.post(login_url, {"username":"user1","password":"pass123"})
        self.assertIn("access", login_resp.data)