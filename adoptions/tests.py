from django.test import TestCase
from rest_framework.test import APITestCase
from userz.models import CustomUser
from pets.models import Pet
from .models import AdoptionRequest

# Create your tests here.
class AdoptionTests(APITestCase):
    def setUp(self):
        self.shelter = CustomUser.objects.create_user(username="shelter1", password="pass", is_shelter=True)
        self.user = CustomUser.objects.create_user(username="user1", password="pass")
        self.pet = Pet.objects.create(name="Buddy", type="Dog", breed="Labrador", age=3, shelter=self.shelter)
        self.client.force_authenticate(user=self.user)

    def test_create_adoption_request(self):
        resp = self.client.post("/api/adoptions/", {"pet": self.pet.id})
        self.assertEqual(resp.status_code, 201)