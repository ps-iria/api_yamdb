from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.CharField()
    confirmation_code = serializers.CharField(allow_blank=False,
                                              write_only=True)

    class Meta:
        model = User
        fields = (
            'confirmation_code',
            'email',
        )
