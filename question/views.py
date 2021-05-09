from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.contenttypes.models import ContentType
from .models import Question, Answer, Comment
from .serializers import QuestionSerializer, CommentSerializer
from django.db.models import Q
import math


# ToDo 글 작성
# ToDo 댓글 작성


@api_view(['GET'])
@permission_classes([AllowAny])
def post_list(request):
    if request.method != 'GET':
        return

    parameter = request.query_params.dict()
    Question.objects.filter()

    try:
        page = int(parameter['page'])  # 페이지 숫자, 페이지에는 10 개의 글을 보여주는 것으로 간주
        view_count = 10
        keyword = ('keyword' in parameter) and parameter['keyword'] or ''  # 검색 기능
    except Exception as e:
        return Response(e.args, status=status.HTTP_400_BAD_REQUEST)

    end_index = page * view_count
    start_index = end_index - view_count
    total_page = {"total_page":  math.ceil(Question.objects.filter().count() / view_count)}

    result = Question.objects \
        .filter(Q(subject__contains=keyword) | Q(content__contains=keyword)) \
        .order_by('-id')[start_index:end_index]

    json_result = QuestionSerializer(result, many=True).data
    json_result.insert(0, total_page)

    return Response(json_result, status=status.HTTP_200_OK)


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
