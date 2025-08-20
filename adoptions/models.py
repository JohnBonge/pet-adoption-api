from django.db import models
from django.conf import settings
from pets.models import Pet

# Create your models here.
class AdoptionRequest(models.Model):
    # FK to Pet without importing Pet directly
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(
        "pets.Pet",  # app_name.ModelName
        on_delete=models.CASCADE,
        related_name="adoptions"
    )

    # FK to your custom user model
    adopter = models.ForeignKey(
        "userz.CustomUser",  # app_name.ModelName
        on_delete=models.CASCADE,
        related_name="adoptions"
    )

    adoption_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adopter} → {self.pet} ({self.status})"