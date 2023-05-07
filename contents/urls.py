from django.urls import path, include
from rest_framework.routers import DefaultRouter

from contents.views import ContentListCreate, ContentDetail, ContentPublish, ShareContentView, \
    RetrieveSharedContentView, ListSharedContentView, FeedbackViewSet

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename="feedback")

urlpatterns = [
    path('create/', ContentListCreate.as_view(), name='content-create'),
    path('<uuid:pk>/', ContentDetail.as_view(), name='content'),
    path('<uuid:pk>/publish/', ContentPublish.as_view(), name="content-publish"),
    path('<uuid:pk>/share/<uuid:share_with>/', ShareContentView.as_view(), name='share-content'),
    path('<uuid:pk>/shared/', RetrieveSharedContentView.as_view(), name="shared-with-content"),
    path('shared/', ListSharedContentView.as_view(), name='all-shared-with'),
    # path('', include(router.urls)),
    path('<uuid:content_id>/', include(router.urls))

]
