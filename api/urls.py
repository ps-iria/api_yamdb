from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import TitleViewSet, CategoryViewSet,GenreViewSet

router = DefaultRouter()
router.register(
    'users',
    views.UserViewSet,
    basename='users'
)
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router.urls)),
]
