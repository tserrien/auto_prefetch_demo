from django.contrib import admin
from .models import Author, Comment


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "dob"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "created_on", "get_post", "get_username"]

    @admin.display(description="username")
    def get_username(self, obj: Comment) -> str:
        return obj.owner.username

    @admin.display(description="post")
    def get_post(self, obj: Comment) -> str:
        return obj.posted_under.title
