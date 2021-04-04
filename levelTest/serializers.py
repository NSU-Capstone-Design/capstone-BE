from rest_framework import serializers
from account.models import User
from levelTest.models import TestProblem, Score
from problemInfo.serializers import ProblemSerializer


class TestProblemSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()

    class Meta:
        model = TestProblem
        fields = ["number", "user", "weight", "problem", "evaluation", "id"]


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ["user", "score"]
