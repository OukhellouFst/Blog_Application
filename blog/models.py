from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#add custom manager published 
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    # define a status for the blog (publishded or Draft)
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    objects = models.Manager() # the default manger
    published = PublishedManager() # Our custom manager

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')

    # define an order ( when no order applied)
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
