import pytest

from pytest_django.asserts import assertNumQueries
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db

# This is where testing get's murky.

# Testing is mostly interesting on the list-views as that's where most admin surfaces struggle


def test_author_admin(admin_user, admin_client, comments):
    # 1 auth query to get session cookies
    # 1 to get auth user details
    # 2 random queries for counts baked into eachadmin page
    # 1 query to fetch the N records on the list view _without_ any related models

    admin_client.force_login(admin_user)

    url = reverse("admin:autoprefetch_author_changelist")

    with assertNumQueries(5):
        admin_client.get(url)


def test_author_detail_admin(admin_user, admin_client, comments):
    # 6 = 2 session save points, 1 auth user query, 1 cookie query, 1 content type
    # + 1 actual query for the requested object.
    admin_client.force_login(admin_user)

    url = reverse("admin:autoprefetch_author_change", kwargs={"object_id": 1})

    with assertNumQueries(6):
        admin_client.get(url)


def test_comment_list_admin(admin_user, admin_client, comments):
    # 7 = 1 for session cookie, 1 for auth user, 2 random counts for baked-in element counts that doesn't seem to be reused
    # 1 for comments, 1 for commenter username, 1 for post title
    admin_client.force_login(admin_user)

    url = reverse("admin:autoprefetch_comment_changelist")

    with assertNumQueries(6):
        admin_client.get(url)
