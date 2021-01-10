from rest_framework import serializers

from project.models import *

class ProbManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbManage
        fields = [
            'user',
            'solbed_check',
            'marked_check',
            'problem'
        ]