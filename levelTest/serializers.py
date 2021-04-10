from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import User
from levelTest.models import TestProblem, Score
from problemInfo.serializers import ProblemSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'nickname', 'level', 'expert_user']


class TestProblemSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()

    class Meta:
        model = TestProblem
        fields = ["number", "user", "weight", "problem", "evaluation", "id"]


class CreateTestProblemSerializer(serializers.Serializer):
    num = serializers.IntegerField(required=True)
    user = serializers.IntegerField(required=True)
    weight = serializers.IntegerField(required=True)
    prob_num = serializers.IntegerField(required=True)

    def validate_prob_num(self, value):
        check = TestProblem.objects.filter(id=value).first()
        if check is None:
            raise ValidationError("problem doesn't exist")
        return value

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["user"])
        testProb = TestProblem.objects.create(
            number=validated_data["num"],
            user=user,
            weight=validated_data["weight"],
            problem_id=validated_data["prob_num"]
        )
        testProb.save()
        return testProb


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ["user", "score"]
