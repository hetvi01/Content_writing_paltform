from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from twitterTrends.constants import DUMMY_TRENDING_TOPIC
from twitterTrends.tweety_api import api


# Create your views here.
class TrendingTopic(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            trends = api.trends_place(pk)
            trending_topics = [t['name'] for t in trends[0]['trends']]
            return Response({"topics": trending_topics}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"topics": DUMMY_TRENDING_TOPIC}, status=HTTP_200_OK)
