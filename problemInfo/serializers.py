from rest_framework import serializers
from .models import ProblemInfo

class ProblemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemInfo
        fields = '__all__'
