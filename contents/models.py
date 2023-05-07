
from django.db import models

from common.models import Common, UUID
from writers.models import Writer


class Content(UUID, Common):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=255)
    body = models.TextField()
    genre = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    shared_with = models.ManyToManyField(Writer, related_name='shared_content')


class Feedback(Common, UUID):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='feedback')
    comment = models.TextField()

