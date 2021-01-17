from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentViewSet
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    registration, get_token, UserViewSet)
from .views import ReviewViewSet, CommentViewSet

from . import views

router = DefaultRouter()
router.register("users", views.UserViewSet)
router.register("titles", views.TitleViewSet)
router.register("categories", views.CategoriesViewSet)
router.register("genres", views.GenresViewSet)

router.register(
    'users',
    views.UserViewSet,
    basename='users'
)
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/auth/email/', registration),
    path('v1/auth/token/', get_token),
]
