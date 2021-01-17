from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ValidationError
from .models import User, Category, Title, Review, Comment, Genre
    

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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        # lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        # lookup_field = 'slug'

class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        fields = '__all__'
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

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Only one review is allowed')
        return data

    def create(self, validated_data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return Review.objects.create(title=title, author=author, **validated_data)

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]
        read_only_fields = ["review"]
