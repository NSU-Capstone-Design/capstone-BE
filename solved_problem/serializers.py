from rest_framework import serializers
from .models import SolvedProblem


class SolvedProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolvedProblem
        fields = '__all__'
