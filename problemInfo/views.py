from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import ProblemInfo
from .serializers import ProblemInfoSerializer


class ProblemInfoView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        serializer = ProblemInfoSerializer(ProblemInfo.objects.all(), many=True)
        return Response(serializer.data)


class ProblemDetailView(APIView):
    permission_classes = (AllowAny,)
    def get_object(self, pk):
        prob = get_object_or_404(ProblemInfo, pk=pk)
        return prob

    def get(self, request, pk):
        prob = self.get_object(pk)
        serializer = ProblemInfoSerializer(prob)
        return Response(serializer.data)
