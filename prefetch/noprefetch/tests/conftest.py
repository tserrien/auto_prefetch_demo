import pytest
from django.db.models import QuerySet
from mixer.backend.django import mixer

from ..models import Author, Post, Commenter, Comment


def authors() -> QuerySet[Author]:
    return mixer.cycle(10).blend(Author)


def commenters() -> QuerySet[Commenter]:
    return mixer.cycle(100).blend(Commenter)


def posts() -> QuerySet[Post]:
    authors()
    return mixer.cycle(100).blend(Post, author=mixer.SELECT)


@pytest.fixture
def noprefetch_comments() -> QuerySet[Comment]:
    commenters()
    posts()
    return mixer.cycle(1500).blend(Comment, owner=mixer.SELECT, posted_under=mixer.SELECT)
