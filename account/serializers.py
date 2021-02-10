from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

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


class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user_id = data.get("user_id", None)
        password = data.get("password", None)
        user = authenticate(user_id=user_id, password=password)

        if user is None:
            return {
                'user_id': 'None'
            }
        try:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                '해당 계정이 존재하지 않습니다.'
            )
        return {
            'user_id': user.user_id,
            'token': token
        }
