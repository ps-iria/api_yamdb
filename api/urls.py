from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    ]