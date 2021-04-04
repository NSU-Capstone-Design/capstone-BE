from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import ProblemInfo
from .serializers import ProblemInfoserializer


class ProblemPost(generics.ListCreateAPIView):
    queryset = ProblemInfo.objects.all()
    serializer_class = ProblemInfoserializer


class TestProblem(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
