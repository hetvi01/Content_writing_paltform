from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from contents.models import Content, Feedback


class ContentSerializer(ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'genre', 'status', 'created_by', 'created_at', 'shared_with']
        extra_kwargs = {'status': {'read_only': True}, 'shared_with': {'read_only': True}}


class FeedbackSerializer(ModelSerializer):
    content = serializers.ReadOnlyField(source='content.title')

    class Meta:
        model = Feedback
        fields = "__all__"


class SharedContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'genre', 'body']
