from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
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
from .serializers import UserSerializer, UserCreateSerializer, ConfirmationCodeSerializer



