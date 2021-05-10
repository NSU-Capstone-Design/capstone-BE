from rest_framework import serializers

from account.serializers import UserSerializer
from . import models


class QuestionSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user_id.user_id')
    nickname = serializers.ReadOnlyField(source='user_id.nickname')

    class Meta:
        model = models.Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user_id.user_id')
    nickname = serializers.ReadOnlyField(source='user_id.nickname')

    class Meta:
        model = models.Answer
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True, method_name="get_reply")
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = '__all__'

    def get_reply(self, obj):
        parent_comments = models.Comment.objects.filter(reply_to=obj.id)
        
        serializer = self.__class__(parent_comments, many=True)
        serializer.bind('', self)
        return serializer.data
