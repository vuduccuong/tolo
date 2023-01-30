from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from tolo_core.view_mixin.jwt_view import JwtAuthViewSet
from tolo_post.serializers.post import PostSerializer, PostDetailSerializer
from tolo_post.services.post import PostService


class PostViewSet(JwtAuthViewSet):
    paginator = LimitOffsetPagination()

    def list(self, request):
        user = request.user
        posts = PostService.get_posts(user_id=user.id)
        serializer = PostSerializer(
            self.paginator.paginate_queryset(posts, request), many=True
        )
        return self.paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        post = PostService.get_post_detail(pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostDetailSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
