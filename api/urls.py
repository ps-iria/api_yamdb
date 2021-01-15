from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    registration, get_token, UserViewSet)

router = DefaultRouter()
router.register(
    'users',
    UserViewSet,
    basename='users'
)
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/auth/email/', registration),
    path('v1/auth/token/', get_token),
]
