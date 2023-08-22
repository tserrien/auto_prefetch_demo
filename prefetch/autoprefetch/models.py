import auto_prefetch
from django.db import models
from django.utils.timezone import now


# Regular models
class Author(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()


class Commenter(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()


# Prefetch models
class Post(auto_prefetch.Model):
    author = auto_prefetch.ForeignKey(
        Author, on_delete=models.DO_NOTHING, related_name="posts"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()

    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Posts"


class Comment(auto_prefetch.Model):
    created_on = models.DateTimeField(default=now)
    body = models.TextField(max_length=1000)
    owner = auto_prefetch.ForeignKey(
        Commenter, on_delete=models.DO_NOTHING, related_name="comments"
    )
    posted_under = auto_prefetch.ForeignKey(
        Post, on_delete=models.DO_NOTHING, related_name="comments"
    )

    class Meta(auto_prefetch.Model.Meta):
        # This only exists so the meta subclass inheritance is used
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
