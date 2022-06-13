import os

from django.contrib.auth.models import User
from django.db import models
from django.utils.deconstruct import deconstructible
# from house.models import House


@deconstructible
class GenerateProfileImagePath(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, instance, filename):
        ext = filename.split("_"[-1])
        path = f"media/accounts/{instance.user.id}/images/"
        name = f"profile_image.{ext}"
        return os.path.join(path, name)


UserProfileImagePath = GenerateProfileImagePath()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=UserProfileImagePath, blank=True, null=True)
    house = models.ForeignKey("house.House", related_name="members", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"
