from rest_framework import serializers

from .models import User, Category, Title, Review, Comment, Genre
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategoryToTitle(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = CategorySerializer(obj)
        return serializer.data


class GenreToTitle(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = GenreSerializer(obj)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryToTitle(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )
    genre = GenreToTitle(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)
    
    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]
        read_only_fields = ["review"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'role',
            'email',
            'confirmation_code',
            'bio',
            'first_name',
            'last_name'
        )
        model = User
        extra_kwargs = {'username': {'required': True},
                        'email': {'required': True}
                        }
                        