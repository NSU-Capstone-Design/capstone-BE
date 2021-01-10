from rest_framework import serializers

from project.models import *

class QuestionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPost
        fields = [
            'title',
            'content',
            'code',
            'created_at'
        ]