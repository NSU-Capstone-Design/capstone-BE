from rest_framework import serializers
from . import models


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user_id.user_id')
    nickname = serializers.ReadOnlyField(source='user_id.nickname')

    class Meta:
        model = models.Question
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True, method_name="get_reply")

    class Meta:
        model = models.Comment
        fields = '__all__'

    def get_reply(self, obj):
        parent_comments = models.Comment.objects.filter(reply_to=obj.id)
        
        serializer = self.__class__(parent_comments, many=True)
        serializer.bind('', self)
        return serializer.data
