from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api import views
from .views import CategoryViewSet, GenreViewset, TitleViewset

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewset)
router.register('titles', TitleViewset)


urlpatterns = [
    path('v1/', include(router.urls)),
    ]