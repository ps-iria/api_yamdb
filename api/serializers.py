from django.db.models import fields
from rest_framework import serializers
from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment
    