from django.shortcuts import render
from rest_framework import generics

from .models import ProblemInfo
from .serializers import ProblemSerializer

class ProblemPost(generics.ListCreateAPIView):
    queryset = ProblemInfo.objects.all()
    serializer_class = ProblemSerializer
