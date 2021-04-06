from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import ProblemInfo
from .serializers import ProblemSerializer

from .serializers import ProblemInfoSerializer

class ProblemInfoView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = ProblemInfoSerializer(ProblemInfo.objects.all(), many=True)
        return Response(serializer.data)

