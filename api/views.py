from django.db import IntegrityError
from rest_framework import viewsets, permissions, generics
from rest_framework.serializers import ValidationError
from .models import Review, Comment, Title
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAdminOrModeratorOrOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    pass

class CategoriesViewSet(viewsets.ModelViewSet):
    pass

class GenresViewSet(viewsets.ModelViewSet):
    pass

class TitleViewSet(viewsets.ModelViewSet):
    pass



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrModeratorOrOwnerOrReadOnly]

    def get_queryset(self):
        title = generics.get_object_or_404(
            Title, id=self.kwargs.get("title_id")
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        try:
            title = generics.get_object_or_404(
                Title, id=self.kwargs.get("title_id")
            )
            serializer.save(title=title, author=self.request.user)
        except IntegrityError:
            raise ValidationError(
                {"detail": "Вы уже оставили отзыв на это произведение."}
            )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrModeratorOrOwnerOrReadOnly]

    def get_queryset(self):
        review = generics.get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = generics.get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )
        serializer.save(review=review, author=self.request.user)
