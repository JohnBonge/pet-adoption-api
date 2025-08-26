from django.db import models
from django.conf import settings
from pets.models import Pet

# Create your models here.
class AdoptionRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="adoptions"
    )
    pet = models.ForeignKey(
        "pets.Pet",
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
    decision_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} → {self.pet} ({self.status})"