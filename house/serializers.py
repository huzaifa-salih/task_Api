from rest_framework import serializers

from house.models import House


class HouseSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)
    members = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="profile-detail")
    manager = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")

    class Meta:
        model = House
        fields = (
            "url",
            "id",
            "name",
            "image",
            "created_on",
            "description",
            "manager",
            "members_count",
            "members",
            "points",
            "completed_tasks_count",
            "notcompleted_tasks_count",
        )
        read_only_fields = ("points", "completed_tasks_count", "notcompleted_tasks_count")
