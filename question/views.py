from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import User, Question, Answer, Comment
from .serializers import QuestionSerializer, AnswerSerializer, CommentSerializer
from django.db.models import Q
import math
import jwt


# 글 작성
class QuestionWriteView(APIView):
    permission_classes(IsAuthenticated, )

    @staticmethod
    def get_object(request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]
        if token:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                return User.objects.get(id=user_pk)
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Login status error", status=status.HTTP_401_UNAUTHORIZED)

    # 질문글 작성 Serializing
    @staticmethod
    def make_question(request):
        try:
            request_data = {
                'user_id': request.user.id,
                'subject': request.data['subject'],
                'content': request.data['content'],
                'prob_num': request.data['problem'],
            }
            question = QuestionSerializer(data=request_data)
        except LookupError:
            question = None
        return question

    # 답변글 작성 Serializing
    @staticmethod
    def make_answer(request):
        try:
            request_data = {
                'user_id': request.user.id,
                'content': request.data['content'],
                'question': request.data['question'],
            }
            answer = AnswerSerializer(data=request_data)
        except LookupError:
            answer = None
        return answer

    # 댓글 작성 Serializing
    @staticmethod
    def make_comment(request):
        try:
            request_data = {
                'user_id': request.user.id,
                'content': request.data['content'],
                'object_id': request.data['object_id'],
                'content_type': ContentType.objects.get_for_model(Question).id,
                'reply_to': None,
            }
            comment = CommentSerializer(data=request_data)
        except LookupError:
            comment = None
        return comment

    def post(self, request):
        if not self.get_object(request):
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        # choose writing type as request element
        def crossroad(x): return x in request.data
        if crossroad('problem'):
            # 게시글 작성
            serializer = self.make_question(request)
        elif crossroad('question'):
            # 답변 작성
            serializer = self.make_answer(request)
        elif crossroad('reply_to'):
            # 댓글 작성
            serializer = self.make_comment(request)
        else:
            serializer = None

        # if data isn`t serialized as well then raise error
        if serializer is None:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        # let`s insert data
        if serializer.is_valid():
            serializer.save()
            ret_status = status.HTTP_201_CREATED
        else:
            ret_status = status.HTTP_400_BAD_REQUEST
        return Response(None, status=ret_status)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def post_content(request):
    parameter = request.query_params['id']

    # 질문 게시글
    question_post = Question.objects.get(id=parameter)
    question_json = QuestionSerializer(question_post).data

    # 질문 댓글들 가져오기
    content_object = ContentType.objects.get_for_model(Question)
    question_comments = Comment.objects.filter(object_id=question_post.id, content_type=content_object)
    question_comments = CommentSerializer(question_comments, many=True).data
    question_json["comments"] = question_comments

    # 답변 게시글
    answer_posts = Answer.objects.filter(question=question_post).order_by('id')
    answer_json = AnswerSerializer(answer_posts, many=True).data

    # 답변 댓글들 가져오기
    content_object = ContentType.objects.get_for_model(Answer)
    for answer_post in answer_json:
        print(answer_post)
        answer_comments = Comment.objects.filter(object_id=answer_post['id'], content_type=content_object)
        answer_comments = CommentSerializer(answer_comments, many=True).data
        answer_post["comments"] = answer_comments

    question_json["answers"] = answer_json

    return Response(question_json, status=status.HTTP_200_OK)


# 질문 게시글 목록 불러오기
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def post_list(request):
    if request.method != 'GET':
        return

    parameter = request.query_params.dict()

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


# 게시글에 대한 댓글 목록 불러오기
@api_view(['GET', 'POST'])
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
