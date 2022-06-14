import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible

NOT_COMPLETED = "NC"
COMPLETED = "C"
TASK_STATUS_CHOICES = [
    (NOT_COMPLETED, "Not completed"),
    (COMPLETED, "Completed"),
]


@deconstructible
class GenarateAttachmentsPathFile(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split("_")[-1]
        path = "media/tasks/ {} /attachments".format(instance.task.id)
        name = "{}.{}".format(instance.id, ext)
        return os.path.join(path, name)


ATTACHMENT_FILE_PATH = GenarateAttachmentsPathFile()


class Task(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("users.Profile", blank=True, null=True, on_delete=models.SET_NULL, related_name="created_tasks")
    completed_by = models.ForeignKey("users.Profile", blank=True, null=True, on_delete=models.SET_NULL, related_name="completed_tasks")
    task_list = models.ForeignKey("task.TaskList", on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=TASK_STATUS_CHOICES, default=NOT_COMPLETED)

    def __str__(self):
        return "{} | {}".format(self.id, self.name)


class TaskList(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(auto_now=True)
    house = models.ForeignKey("house.House", related_name="lists", on_delete=models.CASCADE)
    created_by = models.ForeignKey("users.Profile", blank=True, null=True, on_delete=models.SET_NULL, related_name="lists")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=TASK_STATUS_CHOICES, default=NOT_COMPLETED)

    def __str__(self):
        return "{} | {}".format(self.id, self.name)


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=ATTACHMENT_FILE_PATH)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")

    def __str__(self):
        return "{} | {}".format(self.id, self.task)
