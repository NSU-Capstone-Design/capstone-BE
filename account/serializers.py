from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import User
# from levelTest.models import TestProblem
# from problemInfo.models import ProblemInfo
from django.contrib.auth import get_user_model
from levelTest.serializers import CreateTestProblemSerializer

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
    def validate_user_id(self, value):
        check_id = User.objects.filter(user_id=value).first()
        if check_id is not None:
            raise ValidationError({
                'message': 'duplicate ID',
                'code': True
            })
        return value

    def validate_email(self, value):
        check_email = User.objects.filter(email=value).first()
        if check_email is not None:
            raise ValidationError({
                'message': 'duplicate email',
                'code': True
            })
        return value

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            user_id=validated_data['user_id'],
            nickname=validated_data['nickname'] if validated_data['nickname'] else "user"
        )
        user.set_password(validated_data['password'])
        user.save()
        for prob in testProbs:
            prob["user"] = user.id
            testProbSerializer = CreateTestProblemSerializer(data=prob)
            if not testProbSerializer.is_valid():
                errorList = testProbSerializer.errors
                print(errorList)
                select = list(errorList.keys())[0]
                print(select, "last")
                if errorList[select]['code']:
                    User.delete(user)
                    raise serializers.ValidationError(errorList)

            testProbSerializer.save()

        return user

    # def updata(self, validated_data):


# testProbs = [
#     {
#         "num": 1,
#         "weight": 3,
#         "prob_num": 15733
#     },
#     {
#         "num": 2,
#         "weight": 3,
#         "prob_num": 14928
#     },
#     {
#         "num": 3,
#         "weight": 3,
#         "prob_num": 15727
#     },
# ]

testProbs = [
    {
        "num": 1,
        "weight": 1,
        "prob_num": 10172
    },
    {
        "num": 2,
        "weight": 2,
        "prob_num": 14681
    },
    {
        "num": 3,
        "weight": 3,
        "prob_num": 2439
    },
    {
        "num": 4,
        "weight": 4,
        "prob_num": 2577
    },
    {
        "num": 5,
        "weight": 5,
        "prob_num": 2869
    },
    {
        "num": 6,
        "weight": 6,
        "prob_num": 1018
    },
    {
        "num": 7,
        "weight": 7,
        "prob_num": 10845
    },
    {
        "num": 8,
        "weight": 8,
        "prob_num": 2606
    },
    {
        "num": 9,
        "weight": 9,
        "prob_num": 1912
    },
    {
        "num": 10,
        "weight": 10,
        "prob_num": 1927
    },
    {
        "num": 11,
        "weight":11,
        "prob_num": 1753
    },
    {
        "num": 12,
        "weight": 12,
        "prob_num": 1922
    },
    {
        "num": 13,
        "weight": 13,
        "prob_num": 1613
    },
    {
        "num": 14,
        "weight": 14,
        "prob_num": 1753
    },
    {
        "num": 15,
        "weight": 15,
        "prob_num": 2585
    },
]
