from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Question, Answer, Comment
from .serializers import QuestionSerializer, CommentSerializer
# from django.core import serializers
# from django.http import HttpResponse
# from django.conf import settings
# from .models import User
# from .serializers import UserSerializer, UserCreateSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def post_list(request):
    if request.method != 'GET':
        return

    return Response({"message": "ok", "code": 1}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def post_comment(request):
    parameter = request.query_params.dict()

    post_id = parameter['id']  # 글 인덱스
    post_type = parameter['type']  # 댓글의 부모 글
    post_object = ContentType.objects.none()

    if post_type == 'post':
        post_object = ContentType.objects.get_for_model(Question)  # Question 모델을 부모로 가진 ContentType = 질문에 작성 된 댓글
    elif post_type == 'answer':
        post_object = ContentType.objects.get_for_model(Answer)  # Answer 모델을 부모로 가진 ContentType = 답변에 작성 된 댓글

    try:
        comments = Comment.objects.filter(object_id=post_id, content_type=post_object)
        json_result = CommentSerializer(comments, many=True).data
        return Response(json_result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
