from cloudinary.models import CloudinaryField
from django.db import models
from django_countries.fields import CountryField

from RiseAboveSilence.accounts.models.user_model import CustomUser


class Profile(models.Model):
    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    country = CountryField(
        max_length=3, blank=True, null=True, blank_label="Select a country"
    )

    profile_picture = CloudinaryField(
        "profile_picture",
        blank=True,
        null=True,
    )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.first_name or self.last_name or "Anonymous"
