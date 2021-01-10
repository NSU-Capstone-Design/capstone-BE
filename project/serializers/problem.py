from rest_framework import serializers

from project.models import *

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            'title',
            'content',
            'algorithm',
            'level',
            'exp'
        ]