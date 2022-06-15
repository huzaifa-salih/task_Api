from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework import status as S
from rest_framework.decorators import action
from rest_framework.response import Response
from task.serilaizer import AttachmentSerializer, TaskListSerializer, TaskSerializer
from task.models import COMPLETED, NOT_COMPLETED, Attachment, Task, TaskList
from task.permission import (
    IsAllowedToEditAttachmentElseNone,
    IsAllowedToEditTaskElseNone,
    IsAllowedToEditTaskListElseNone,
)


class TaskListViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
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

    @action(detail=True, methods=["patch"])
    def update_task_status(self, request, pk=None):
        try:
            task = self.get_object()
            profile = request.user.profile
            status = request.data["status"]
            if status == NOT_COMPLETED:
                if task.status == COMPLETED:
                    task.status = NOT_COMPLETED
                    task.completed_on = None
                    task.completed_by = None
                else:
                    raise Exception("Task is already marked as not_completed")
            elif status == COMPLETED:
                if task.status == NOT_COMPLETED:
                    task.status = COMPLETED
                    task.completed_on = timezone.now()
                    task.completed_by = profile
                else:
                    raise Exception("Task is already marked as completed")
            else:
                raise Exception("Incorrect status provided")
            task.save()
            serializer = TaskSerializer(instance=task, contxt={"request": request})
            return Response(serializer.data, status=S.HTTP_200_OK)
        except Exception:
            return Response({"detail": str(Exception)}, status=S.HTTP_400_BAD_REQUEST)


class AttachmentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditAttachmentElseNone]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
