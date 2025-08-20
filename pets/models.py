from django.db import models
from django.conf import settings

# Create your models here.
class Pet(models.Model):
    DOG = "Dog"; CAT = "Cat"
    TYPES = [(DOG, "Dog"), (CAT, "Cat")]
    name = models.CharField(max_length=120)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=120)
    type = models.CharField(max_length=20)
    health_status = models.TextField(blank=True)
    photo = models.ImageField(upload_to="pets/", blank=True, null=True)
    available = models.BooleanField(default=True)
    shelter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pets")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["type", "breed"]),
            models.Index(fields=["available"]),
        ]