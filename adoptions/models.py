from django.db import models
from django.conf import settings

# Create your models here.
class AdoptionRequest(models.Model):
    PENDING = "Pending"; APPROVED = "Approved"; REJECTED = "Rejected"
    STATUS = [(PENDING, "Pending"), (APPROVED, "Approved"), (REJECTED, "Rejected")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adoption_requests")
    pet = models.ForeignKey("pets.Pet", on_delete=models.CASCADE, related_name="adoption_requests")
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    decision_at = models.DateTimeField(blank=True, null=True)