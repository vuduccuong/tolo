from rest_framework import serializers

from tolo_account.serializers.author import AuthorSerializer
from tolo_post.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        exclude = (
            "content",
            "updated_by",
            "created_by",
            "modified_date",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = "__all__"
