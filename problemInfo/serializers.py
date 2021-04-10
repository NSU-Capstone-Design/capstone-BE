from rest_framework import serializers
from .models import ProblemInfo

class ProblemInfoserializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title',
            'level',
            'timeout',
            'memory_limit',
            'submission',
            'correct',
            'correct_people',
            'correct_answer_rate',
            'problem_content',
            'problem_input',
            'problem_output',
        )
        model = ProblemInfo