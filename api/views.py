from rest_framework import viewsets

from .models import Category, Genre, Title


class UserViewSet(viewsets.ModelViewSet):
    pass

class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewset(viewsets.ModelViewSet):
    pass


class TitleViewset(viewsets.ModelViewSet):
    pass
