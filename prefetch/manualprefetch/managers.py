from django.db import models


class CommentManager(models.Manager):
    def prefetched_commenter(self):
        return self.get_queryset().prefetch_related("owner")

    def prefetch_post_and_author(self):
        return (
            self.get_queryset()
            .prefetch_related("posted_under")
            .prefetch_related("posted_under__author")
        )

    def prefetch_post(self):
        return self.get_queryset().prefetch_related("posted_under")
