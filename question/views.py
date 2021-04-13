from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Question, Answer, Comment
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
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

    post_id = parameter['id']
    post_type = parameter['type']
    post_object = ContentType.objects.none()
    if post_type == 'post':
        post_object = ContentType.objects.get_for_model(Question)
    elif post_type == 'comment':
        post_object = ContentType.objects.get_for_model(Comment)

    comments = Comment.objects.filter(object_id=post_id, content_type=post_object)
    get_object_or_404(comments)
    response = serializers.serialize("json", comments)
    return HttpResponse(response, content_type='application/json')
