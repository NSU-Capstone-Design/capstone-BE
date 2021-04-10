from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import jwt
from .models import TestProblem, Score
from .serializers import TestProblemSerializer


class LevelTestProblemListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]

        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                test_problems = TestProblem.objects.filter(user_id=user_pk)
                myTestProblems = TestProblemSerializer(test_problems, many=True).data
                content = {'probs': myTestProblems}
                return Response(content)
            except KeyError as e:
                content = {
                    'message': e
                }
                return Response(content)


class LevelTestProblemView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]

        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                test_problem = TestProblem.objects.get(id=request.data["id"])
                print(test_problem.evaluation)
                test_problem.evaluation = request.data["grade"]
                test_problem.save()
                return Response(status=status.HTTP_200_OK)
            except KeyError as e:
                content = {
                    'message': e
                }
                return Response(content)
