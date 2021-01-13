from rest_framework import viewsets, permissions
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAdmin, IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [IsOwnerOrReadOnly, IsAdmin]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [IsOwnerOrReadOnly, IsAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        review_id = self.kwargs["review_id"]
        queryset = Comment.objects.filter(review=review_id)
        return queryset
