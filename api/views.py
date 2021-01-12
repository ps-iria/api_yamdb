from datetime import datetime
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator, \
    PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer

EMAIL_AUTH = '11@11.11'


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(
        User, email=email, confirmation_code=confirmation_code)
    refresh_tokens = RefreshToken.for_user(user)
    tokens = {'refresh': str(refresh_tokens),
              'access': str(refresh_tokens.access_token), }
    return Response({"message": tokens.items()})


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    email = request.data.get('email')
    username = request.data.get('username')
    if not email:
        return Response({'message': {
            'Ошибка': 'Не указана почта для регистрации'}},
            status=status.HTTP_403_FORBIDDEN)
    code = PasswordResetTokenGenerator()
    user = get_user_model()
    user.email = email
    user.last_login = datetime.now()
    user.password = ''
    confirmation_code = code.make_token(user)
    try:
        query_get, flag = get_user_model().objects.get_or_create(
            email=email,
            defaults={'username': email,
                      'confirmation_code': confirmation_code,
                      'last_login': datetime.now()})
        if not flag:
            return Response({'message': {
                'Ошибка': 'Пользователь с таким email уже существует.'}},
                status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({'message': {
            'Ошибка': 'Ошибка запроса'}}, status=status.HTTP_403_FORBIDDEN)
    send_mail(
        'Подтверждение адреса электронной почты YaTube',
        'Вы получили это письмо, потому что регистрируетесь на ресурсе '
        'YaTube Код подтверждения confirmation_code = '
        + str(confirmation_code),
        settings.DEFAULT_FROM_EMAIL,
        [email, ],
        fail_silently=False, )
    return Response({'message': {
        'ОК': f'Пользователь c email {email} создан успешно. '
              'Код подтверждения отправлен на электронную почту'}})


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
        return Response(serializer.data, status=status.HTTP_200_OK)
