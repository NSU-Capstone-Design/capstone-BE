from rest_framework import serializers
from . import models
from django.contrib.contenttypes.models import ContentType


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['user_id', 'prob_num', 'subject', 'content', 'created_at', 'updated_at']


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
