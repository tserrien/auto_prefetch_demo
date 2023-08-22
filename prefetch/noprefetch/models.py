from django.db import models
from django.utils.timezone import now


class Author(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()


class Commenter(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()


class Post(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.DO_NOTHING, related_name="posts"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()


class Comment(models.Model):
    created_on = models.DateTimeField(default=now)
    body = models.TextField(max_length=1000)
    owner = models.ForeignKey(
        Commenter, on_delete=models.DO_NOTHING, related_name="comments"
    )
    posted_under = models.ForeignKey(
        Post, on_delete=models.DO_NOTHING, related_name="comments"
    )
