import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible

# from users.models import Profile


@deconstructible
class GenerateHouseImagePath(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, instance, filename):
        ext = filename.split("_"[-1])
        path = f"media/house/{instance.id}/images/"
        name = f"main.{ext}"
        return os.path.join(path, name)


HouseImagePath = GenerateHouseImagePath()


class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    image = models.FileField(upload_to=HouseImagePath, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    manager = models.OneToOneField("users.Profile", related_name="manager_house", blank=True, null=True, on_delete=models.SET_NULL)
    points = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)
    notcompleted_tasks_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} | {self.id}"
