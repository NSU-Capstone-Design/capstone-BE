from rest_framework import serializers
from .models import ProblemInfo, IOExam


class IOExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = IOExam
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    ioexam_set = IOExamSerializer(many=True, read_only=True)

    class Meta:
        model = ProblemInfo
        fields = [
            'prob_num',
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
            'ioexam_set',
            'imgurl']
        model = ProblemInfo