import pytest

from pytest_django.asserts import assertNumQueries
from ..models import Comment

pytestmark = pytest.mark.django_db


def test_default_query_no_prefetch(noprefetch_comments):
    # The bog standard fetch-all, no funny business query

    comments = Comment.objects.all()

    with assertNumQueries(1):
        for comment in comments:
            print(comment.body)


def test_one_foreign_connection(noprefetch_comments):
    # The differences start to come out here.
    # Notice the difference compared to both auto-prefetch and the manual version!

    comments = Comment.objects.all()

    with assertNumQueries(1501):
        for comment in comments:
            print(comment.owner)


def test_foreign_connection_of_foreign_object(noprefetch_comments):
    # This is where query numbers start to explode

    comments = Comment.objects.all()

    with assertNumQueries(3001):
        for comment in comments:
            print(comment.posted_under.author.name)


