
import pytest
from pytest_django.asserts import assertNumQueries
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


def test_author_list(client, noprefetch_comments):
    # Not expecting any funny business, model has no FK fields
    # Serializer doesn't fetch reverse relationship

    url = reverse("nopref:author-list")

    with assertNumQueries(1):
        client.get(url)


def test_post_detail(client, noprefetch_comments):
    # Post, comments and author with separate query under the hood

    url = reverse("nopref:post-detail", kwargs={"pk": 1})

    with assertNumQueries(3):
        client.get(url)


def test_post_list(client, noprefetch_comments):
    # 1 for posts + 100 related author + 100 for comments

    url = reverse("nopref:post-list")

    with assertNumQueries(201):
        client.get(url)
