from django.urls import path

from twitterTrends.views import TrendingTopic

urlpatterns = [
    path('dashboard/<int:pk>/', TrendingTopic.as_view(), name='content-create'),

]
