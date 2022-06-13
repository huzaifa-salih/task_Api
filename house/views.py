from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from house.models import House
from house.permissions import IsHouseManagerOrNone
from house.serializers import HouseSerializer


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsHouseManagerOrNone]

    @action(detail=True, methods=["post"], name="Join Member")
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if user_profile.house == None:
                user_profile.house = house
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif user_profile in house.members.all():
                return Response({"detail": "This member already in this house."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "This member already in another house."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["post"], name="Leave Member")
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if user_profile.house == None:
                user_profile.house = house
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({"detail": "User not a member in this house."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["post"], name="Remove Member")
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            user_id = request.data.get("user_id", None)
            if user_id == None:
                return Response({"user_id": "Not provided."}, status=status.HTTP_400_BAD_REQUEST)
            user_profile = User.objects.get(pk=user_id).profile()
            houser_members = house.members
            if user_profile in houser_members.all():
                houser_members.remove(user_profile)
                house.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "User not a member in this house."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist as e:
            return Response({"detail": "Provided user_id dose not exist."}, status=status.HTTP_400_BAD_REQUEST)
