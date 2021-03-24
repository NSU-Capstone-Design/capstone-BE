from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from account.models import User
from levelTest.models import TestProblem
from problemInfo.models import ProblemInfo
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'nickname', 'level', 'expert_user']


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    nickname = serializers.CharField(allow_blank=True, default="user")

    # student_id = serializers.CharField(max_length=10)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            user_id=validated_data['user_id'],
            nickname=validated_data['nickname'] if validated_data['nickname'] else "user"
        )
        user.set_password(validated_data['password'])
        print("serializer create")
        user.save()
        for prob in testProbs:
            testProb = TestProblem.objects.create(
                number=prob["num"],
                user=user,
                weight=prob["weight"],
                problem_id=prob["prob_num"]
            )
            testProb.save()
        return user

    # def updata(self, validated_data):


testProbs = [
    {
        "num": 1,
        "weight": 3,
        "prob_num": 15733
    },
    {
        "num": 2,
        "weight": 3,
        "prob_num": 14928
    },
    {
        "num": 3,
        "weight": 3,
        "prob_num": 15727
    },
]
