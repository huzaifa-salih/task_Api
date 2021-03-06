from ssl import create_default_context

from django.http import QueryDict
from platformdirs import user_cache_dir
from requests import request
from rest_framework import mixins, viewsets

from task.models import Attachment, Task, TaskList
from task.permission import (
    IsAllowdToEditAttachmentElseNone,
    IsAllowedToEditTaskElseNone,
    IsAllowedToEditTaskListElseNone,
)
from task.serilaizer import AttachmentSerializer, TaskListSerializer, TaskSerializer


class TaskListViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    # mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = [IsAllowedToEditTaskListElseNone]
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()
        user_profile = self.request.user.profile
        update_queryset = queryset.filter(created_by=user_profile)
        return update_queryset


class AttachmentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    # mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = [IsAllowdToEditAttachmentElseNone]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
