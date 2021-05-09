from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.conf import settings
from account.models import User
from solved_problem.models import SolvedProblem
import jwt


class SolveSuccessView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]
        prob_id = request.data["prob_id"]
        print(prob_id)
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
            SolvedProblem.objects.update_or_create(user_id=int(user_pk), prob_id=prob_id, defaults={'correct': True})
            return Response(status=status.HTTP_200_OK)


class SolvePassView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]
        prob_id = request.data["prob_id"]
        print(prob_id)
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
            SolvedProblem.objects.update_or_create(user_id=int(user_pk), prob_id=prob_id, defaults={'correct': False})
            return Response(status=status.HTTP_200_OK)
