from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator, \
    default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, decorators
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer, UserCreateSerializer, \
    ConfirmationCodeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'username'

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=[IsAuthenticated, ],
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
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user = User.objects.get_or_create(
        email=email,
        username=username,
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Подтверждение адреса электронной почты YamDB',
        'Вы получили это письмо, потому что регистрируетесь на ресурсе '
        'YaTube Код подтверждения confirmation_code = '
        + str(confirmation_code),
        settings.DEFAULT_FROM_EMAIL,
        [email, ],
        fail_silently=False, )
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)
