from rest_framework import serializers

from project.models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'group_id',
            'member',
            'status'
        ]