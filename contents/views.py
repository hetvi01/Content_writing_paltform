from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, \
    ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from contents.constants import CONTENT_CREATED_SUCCESSFULLY, CONTENT_UPDATED_SUCCESSFULLY, \
    CONTENT_PUBLISHED_SUCCESSFULLY
from contents.mixins import ContentOwnershipMixin
from contents.models import Content
from contents.serializers import ContentSerializer, SharedContentSerializer, FeedbackSerializer
from writers.models import Writer


class ContentListCreate(ListCreateAPIView):
    """
        API view to list and create content.
    """
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
            Get queryset based on request parameters.
        """
        current_user = self.request.user
        choice = self.request.query_params.get('choice')
        if choice == 'published':
            return Content.objects.filter(published=True, created_by=current_user)
        elif choice == 'draft':
            return Content.objects.filter(published=False, created_by=current_user)
        else:
            return Content.objects.filter(created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Create a new content object.
        :param request:
        :param args:
        :param kwargs:
        :return: A serialized data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by_id=request.user.id)
        return Response({'message': CONTENT_CREATED_SUCCESSFULLY, 'data': serializer.data}, status=HTTP_201_CREATED)


class ContentDetail(ContentOwnershipMixin, RetrieveUpdateDestroyAPIView):
    """
       Retrieve, update or delete a content instance.
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        This method is used to update tasks
        :param request:
        :param args:
        :param kwargs:
        :return: A serialized data
        """

        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data, 'message': CONTENT_UPDATED_SUCCESSFULLY}, status=HTTP_200_OK)


class ContentPublish(ContentOwnershipMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        This method is used to publish content which is draft
        :param request:
        :param args:
        :param kwargs:
        :return: A serialized data
        """

        content = get_object_or_404(Content, id=pk, created_by=request.user, status='draft')
        content.status = 'published'
        content.save()
        return Response({'message': CONTENT_PUBLISHED_SUCCESSFULLY}, status=HTTP_201_CREATED)


class ShareContentView(ContentOwnershipMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, share_with):
        """
        This method is used to share content to another writer
        :param request:
        :param args:
        :param kwargs:
        :return: A serialized data
        """

        content = self.get_object()
        writer_obj = Writer.objects.get(id=share_with)
        content.shared_with.add(writer_obj)
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=HTTP_200_OK)


class RetrieveSharedContentView(RetrieveAPIView):
    """
        Retrieve shared content
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SharedContentSerializer

    def get_queryset(self):
        return Content.objects.filter(shared_with__id=self.request.user.id, id=self.kwargs.get('pk'))


class ListSharedContentView(ListAPIView):
    """
    List all shared content
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SharedContentSerializer

    def get_queryset(self):
        return Content.objects.filter(shared_with__id=self.request.user.id)


class FeedbackViewSet(ModelViewSet):
    """
     A ViewSet for handling feedback related requests.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def create(self, request, content_id=None):
        """
       Give feedback for the given content.
       :param request:
       :param content_id: The ID of the content for which the feedback is being created.
       :returns: A serialized data
       :raise PermissionDenied: If the requesting user is not authorized to give feedback for the content.
        """
        content = get_object_or_404(Content, id=content_id)
        if request.user not in content.shared_with.all():
            raise PermissionDenied
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, content=content)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def list(self, request, content_id=None):
        content = get_object_or_404(Content, pk=content_id)
        if not content.shared_with.filter(id=request.user.id).exists():
            raise PermissionDenied
        feedback = content.feedback.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data)
