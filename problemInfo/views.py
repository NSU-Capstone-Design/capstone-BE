import jwt
import random
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from account.models import User
from solved_problem.models import SolvedProblem
from .models import ProblemInfo
from .serializers import ProblemSerializer
from django.db.models import Q


class ProbList(generics.ListAPIView):
    permission_classes = (AllowAny,)

    queryset = ProblemInfo.objects.all()
    serializer_class = ProblemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prob_num']


# class ProblemInfoView(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         serializer = ProblemSerializer(ProblemInfo.objects.all(), many=True)
#         return Response(serializer.data)


class ProblemDetailView(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        prob = get_object_or_404(ProblemInfo, pk=pk)
        return prob

    def get(self, request, pk):
        prob = self.get_object(pk)
        serializer = ProblemSerializer(prob)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProblemInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                user = User.objects.get(id=user_pk)
            except Exception as e:
                return Response(e, status.HTTP_400_BAD_REQUEST)
            print('level', user.level)
            userLevelProbs = list(ProblemInfo.objects.filter(level=user.level))
            solvedProblems = SolvedProblem.objects.filter(user=user)
            levelSolvedProblems = []
            print('userLevelProbs', userLevelProbs)
            print(solvedProblems)
            for p in solvedProblems:
                if p.prob.level == user.level:
                    levelSolvedProblems.append(p.prob)

            for lsp in levelSolvedProblems:
                for ulp in userLevelProbs:
                    if lsp.prob_num == ulp.prob_num:
                        print('here')
                        del userLevelProbs[userLevelProbs.index(lsp)]

            if len(userLevelProbs) != 0:
                serializer = ProblemSerializer(userLevelProbs[0])
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                passedProbsQuery = SolvedProblem.objects.filter(Q(user=user) & Q(correct=False))
                passedProbs = []
                for sp in passedProbsQuery:
                    if sp.prob.level == user.level:
                        passedProbs.append(sp.prob)
                if len(passedProbs) == 0:
                    return Response({"user_level": user.level}, status.HTTP_406_NOT_ACCEPTABLE)
                passedProb = random.choice(passedProbs)
                serializer = ProblemSerializer(passedProb)
                ctx = serializer.data
                ctx['user_level'] = user.level

        return Response(ctx, status.HTTP_200_OK)
