from house.models import House
from rest_framework import serializers

from task.models import Attachment, Task, TaskList


class TaskListSerializer(serializers.ModelSerializer):
    house = serializers.HyperlinkedRelatedField(queryset=House.objects.all(), many=False, view_name="house-detail")
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    tasks = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="task-detail")

    class Meta:
        model = TaskList
        fields = ["url", "id", "name", "description", "status", "created_on", "created_by", "house", "tasks"]
        read_only_fields = ["created_on", "status"]


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), many=False, view_name="tasklist-detail")
    attachments = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="attachments-detail")

    class Meta:
        model = Task
        fields = [
            "url", 
            "id",
            "created_on", 
            "completed_on",
            "created_by", 
            "completed_by", 
            "task_list", 
            "name", 
            "description", 
            "status", 
            "attachments",
        ]
        read_only_fields = ["created_on", "created_by", "completed_by", "completed_on"]


class AttachmentSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), many=False, view_name="task-detail")

    class Meta:
        model = Attachment
        fields = ["url", "id", "created_on", "data", "task"]
        read_only_fields = ["created_on"]
