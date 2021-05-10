from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.conf import settings
from solved_problem.models import SolvedProblem
import jwt
from django.db.models import Q

from solved_problem.serializers import SolvedProblemSerializer


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
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
            SolvedProblem.objects.update_or_create(user_id=int(user_pk), prob_id=prob_id, defaults={'correct': False})
            return Response(status=status.HTTP_200_OK)


class MySolvedProbsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]

        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                correctList = SolvedProblem.objects.filter(Q(user=user_pk) & Q(correct=True))
                ctx = SolvedProblemSerializer(correctList, many=True).data
                print(ctx)

                return Response(ctx, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyPassProbsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]

        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                correctList = SolvedProblem.objects.filter(Q(user=user_pk) & Q(correct=False))
                ctx = SolvedProblemSerializer(correctList, many=True).data

                return Response(ctx, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
