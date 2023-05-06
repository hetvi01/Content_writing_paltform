import uuid

from django.db import models
from django.utils.timezone import now

from contentWritingPlatform.settings import AUTH_USER_MODEL


# Create your models here.
class Common(models.Model):
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(AUTH_USER_MODEL,
                                   related_name='%(class)s_createdby', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class UUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True
