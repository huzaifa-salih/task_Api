from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from house import router as HouseApiRouter
from task import router as TaskApiRouter
from users import router as UsersApiRouter

AuthApiUrls = [
    path(r"", include("drf_social_oauth2.urls", namespace="drf")),
]
if settings.DEBUG:
    AuthApiUrls.append(path(r"verify/", include("rest_framework.urls"))),


ApiUrlPatterns = [
    path(r"auth/", include(AuthApiUrls)),
    path(r"accounts/", include(UsersApiRouter.router.urls)),
    path(r"house/", include(HouseApiRouter.router.urls)),
    path(r"task/", include(TaskApiRouter.router.urls)),
]
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(ApiUrlPatterns)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
