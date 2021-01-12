from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'users',
    views.UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
