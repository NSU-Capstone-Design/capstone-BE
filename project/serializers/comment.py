from rest_framework import serializers

from project.models import *

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'postID',
            'content',
            'writer',
            'votes',
            'created_at'
        ]