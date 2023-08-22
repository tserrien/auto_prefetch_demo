import pytest

from pytest_django.asserts import assertNumQueries
from ..models import Comment, Post

pytestmark = pytest.mark.django_db


def test_default_query_no_prefetch(comments):
    # Just like without using auto-prefetch only one query should be executed here

    comments = Comment.objects.all()

    with assertNumQueries(1):
        for comment in comments:
            print(comment.body)


def test_one_foreign_connection(comments):
    # Here we expect auto-prefect to first create a query to execute
    # the .objects.all() query and one more when it detects a related model's fields are accessed.
    # Note the difference in queries executed compared to not using auto-prefetch

    comments = Comment.objects.all()

    with assertNumQueries(2):
        for comment in comments:
            print(comment.posted_under.title)


def test_foreign_connection_of_foreign_object(comments):
    # Here auto-prefetch needs to detect not only one but two relations.

    # Would only 1 or 2 queries be nicer?
    # Yes

    # Does this still eliminate hundreds of useless repetitions of a query?
    # Also yes

    comments = Comment.objects.all()

    with assertNumQueries(3):
        for comment in comments:
            print(comment.posted_under.author.name)


def test_reverse(comments):
    posts = Post.objects.all()

    with assertNumQueries(2):
        for post in posts:
            for comment in post.comments.all():
                print(comment.created_on)

    # Expected behaviour:
    # posts = Post.objects.prefetch_related("comments")
    # with assertNumQueries(2):
    #     for post in posts:
    #         for comment in post.comments.all():
    #             print(comment.created_on)