from datetime import datetime

from django.db.models import Avg
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Title, Category, Genre, User
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение JWT-токена"""
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(
        User, email=email, confirmation_code=confirmation_code)
    refresh_tokens = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh_tokens),
        'access': str(refresh_tokens.access_token),
    }
    return Response({"message": tokens.items()})


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    """Регистрация пользователя и получение confirmation_code"""
    email = request.data.get('email')
    username = request.data.get('username')
    if not email:
        return Response(
            {
                'message':
                    {
                        'Ошибка': 'Не указана почта для регистрации'
                    }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    token = PasswordResetTokenGenerator()
    user = get_user_model()
    user.email = email
    user.last_login = datetime.now()
    user.password = ''
    confirmation_code = token.make_token(user)
    try:
        query_get, flag = get_user_model().objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'confirmation_code': confirmation_code,
                'last_login': datetime.now()})
        if not flag:
            return Response(
                {
                    'message':
                        {
                            'Ошибка': ('Пользователь с таким email '
                                       'уже существует.')
                        }
                },
                status=status.HTTP_403_FORBIDDEN
            )
    except:
        return Response(
            {
                'message':
                    {
                        'Ошибка': 'Ошибка запроса'
                    }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    send_mail(
        'Подтверждение адреса электронной почты yamdb',
        'Вы получили это письмо, потому что регистрируетесь на ресурсе '
        'yamdb Код подтверждения confirmation_code = '
        + str(confirmation_code),
        settings.DEFAULT_FROM_EMAIL,
        [email, ],
        fail_silently=False,
    )
    return Response(
        {
            'message':
                {
                    'ОК': f'Пользователь c email {email} успешно создан. '
                          'Код подтверждения отправлен на электронную почту'
                }
        }
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'username'

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request):
        serializer = UserSerializer(request.user, many=False)
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                'message': 'Пользователь удален'
            },
            status=status.HTTP_204_NO_CONTENT
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    lookup_field = 'slug'
    http_method_names = ['get', 'create', 'delete']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    lookup_field = 'slug'
    http_method_names = ['get', 'create', 'delete']
