from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Create your models here.


class LandOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Land(BaseModel):
    class LandStatus(models.TextChoices):
        SOLD = "S", _("Sold")
        NEGOTIATION = "N", _("Negotiations")

    place = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey(LandOwner, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, choices=LandStatus.choices, default=LandStatus.NEGOTIATION
    )
