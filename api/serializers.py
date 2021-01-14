from rest_framework import serializers
from .models import Review, Comment, User


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "pub_date"]
        read_only_fields = ["title"]


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]
        read_only_fields = ["review"]
    
