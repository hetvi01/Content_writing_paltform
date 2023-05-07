from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from contents.models import Content


class ContentOwnershipMixin(object):
    """
    Mixin to check  requesting user is the owner of the content.
    If the requesting user is not the owner, then a PermissionDenied exception is raised.
    """
    def get_object(self):
        obj = get_object_or_404(Content, pk=self.kwargs["pk"])
        if obj.created_by != self.request.user:
            raise PermissionDenied
        return obj
