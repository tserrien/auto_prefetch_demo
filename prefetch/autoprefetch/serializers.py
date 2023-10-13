from rest_framework import serializers

from .models import Comment, Commenter, Author, Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    # the package can deal with reverse relationships too
    class Meta:
        model = Comment
        fields = ["body", "created_on"]


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"


class CommenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commenter
        fields = "__all__"
