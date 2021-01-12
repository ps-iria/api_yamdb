from rest_framework import serializers

from .models import Genre, Category, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        pass


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        pass


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        pass
