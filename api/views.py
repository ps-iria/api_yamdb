from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from .models import Title, Category, Genre
from .filters import TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #permission_classes = []
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    lookup_field = 'slug'
    http_method_names = ['get', 'create', 'delete']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializer
    #permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    lookup_field = 'slug'
    http_method_names = ['get', 'create', 'delete']
