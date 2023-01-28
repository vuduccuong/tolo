from rest_framework.pagination import LimitOffsetPagination

from tolo_core.view_mixin.jwt_view import JwtAuthViewSet
from tolo_post.serializers.post import PostSerializer
from tolo_post.services.post import PostService


class PostViewSet(JwtAuthViewSet):
    def list(self, request):
        paginator = LimitOffsetPagination()
        posts = PostService.get_posts()
        serializer = PostSerializer(
            paginator.paginate_queryset(posts, request), many=True
        )
        return paginator.get_paginated_response(serializer.data)
