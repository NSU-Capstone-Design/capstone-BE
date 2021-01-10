from rest_framework import serializers

from project.models import *

class IOExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = IOExam
        fields = [
            'input',
            'output'
        ]