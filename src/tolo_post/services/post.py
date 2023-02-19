from django.db.models import QuerySet

from tolo_core.search.base import SearchResult
from tolo_core.search.body_builder import BodyBuilder
from tolo_post.models import Post
from tolo_post.search import PostElasticSearch


class PostService:
    @classmethod
    def get_posts(cls, user_id: int, **kwargs) -> SearchResult:
        body = BodyBuilder()
        q = kwargs.pop("q", "")
        if q:
            body.add_match("title", q)

        return PostElasticSearch().search(body=body.build(), **kwargs)

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
