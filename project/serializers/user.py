from rest_framework import serializers

from project.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'ID',
            'password',
            'nickname',
            'csrf',
            'login_token'
        ]