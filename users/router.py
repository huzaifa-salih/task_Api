from rest_framework import routers
from users.views import ProfileViewSet, UserViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register("users", UserViewSet)
router.register("profiles", ProfileViewSet)
