from rest_framework import serializers

from project.models import *

class MyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'user',
            'question'
        ]