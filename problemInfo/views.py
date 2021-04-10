from django.shortcuts import render
from rest_framework import generics

from .models import ProblemInfo

from .serializers import ProblemSerializer

from .serializers import ProblemInfoSerializer

class ProblemInfoView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = ProblemInfoSerializer(ProblemInfo.objects.all(), many=True)
        return Response(serializer.data)

