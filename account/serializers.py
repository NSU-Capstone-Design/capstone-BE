from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from account.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)

    # student_id = serializers.CharField(max_length=10)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            user_id=validated_data['user_id'],
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password'])

        user.save()
        return user
