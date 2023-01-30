from django.db.models import QuerySet
from tolo_post.models import Post


class PostService:
    @classmethod
    def get_posts(cls, user_id: int) -> QuerySet[Post]:
        return Post.objects.select_related("author").filter(author_id=user_id)

    @classmethod
    def get_post_detail(cls, pk) -> QuerySet[Post] | None:
        try:
            is_pk = False
            try:
                pk = int(pk)
                is_pk = True
            except:
                pass
            if is_pk:
                return Post.objects.get(id=pk)

            return Post.objects.get(slug__exact=pk)
        except Post.DoesNotExist:
            return None
