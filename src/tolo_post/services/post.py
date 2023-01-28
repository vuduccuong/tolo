from django.db.models import QuerySet

from tolo_post.models import Post


class PostService:
    @classmethod
    def get_posts(cls) -> QuerySet[Post]:

        return Post.objects.select_related("author").all()
