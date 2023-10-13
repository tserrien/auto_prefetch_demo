import pytest

from pytest_django.asserts import assertNumQueries
from ..models import Comment

pytestmark = pytest.mark.django_db


def test_default_query_no_prefetch_no_manager(comments):
    # The bog standard fetch-all, no funny business query

    comments = Comment.objects.all()

    with assertNumQueries(1):
        for comment in comments:
            print(comment.body)


def test_default_query_no_prefetch_manager(comments):
    # In case you use the prefetch related with the manager
    # (typo, accident, oversight, 2am deadline crunch, whatever)
    # an extra query is introduced. Not great, not terrible.
    # An extra query vs N extra query is still not the same.
    # I'd consider this to be a low likelihood mistake, a code review should catch this.

    comments = Comment.objects.prefetched_commenter()

    with assertNumQueries(2):
        for comment in comments:
            print(comment.body)


def test_one_foreign_connection(comments):
    # Functionally equivalent to using auto-prefetch BUT needs a custom manager added
    # In an ideal world that manager would also needs tests, which is time, time is money, etc.

    comments = Comment.objects.prefetched_commenter()

    with assertNumQueries(2):
        for comment in comments:
            print(comment.owner)


def test_foreign_connection_of_foreign_object(comments):
    # Again, functionally equivalent to using auto-prefetch with all the downsides mentioned above

    comments = Comment.objects.prefetch_post_and_author()

    with assertNumQueries(3):
        for comment in comments:
            print(comment.posted_under.author.name)


def test_prefetch_with_manager_and_accessing_second_foreign_model(comments):
    # This highlights a downside of the custom manager approach.
    # If a premade queryset doesn't exist for a usecase the 1+N query problem can return

    comments = Comment.objects.prefetch_post()

    with assertNumQueries(102):
        for comment in comments:
            print(comment.posted_under.author.name)
