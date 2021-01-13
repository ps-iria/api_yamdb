from rest_framework import serializers

from .models import User


# def required(value):
#     if value is None:
#         raise serializers.ValidationError('This field is required')


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(validators=[required])

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
