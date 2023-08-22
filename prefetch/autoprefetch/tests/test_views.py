import pytest
from pytest_django.asserts import assertNumQueries
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


def test_author_list(client, prefetch_comments):
    # Not expecting any funny business, model has no FK fields
    # Serializer doesn't fetch reverse relationship

    url = reverse("autopref:author-list")

    with assertNumQueries(1):
        client.get(url)


def test_post_detail(client, prefetch_comments):
    # This is where the fun begins
    # Author is fetched via a reverse relationship
    # Comments still broken, _but_ one query saved
    # Victory?

    url = reverse("autopref:post-detail", kwargs={"pk": 1})

    with assertNumQueries(2):
        client.get(url)


def test_post_list(client, prefetch_comments):
    # 1 for all posts + 1 for all authors + 100 for comments of each post

    url = reverse("autopref:post-list")

    with assertNumQueries(102):
        client.get(url)
