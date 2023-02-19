from rest_framework import status
from rest_framework.response import Response

from tolo_core.helpers.utils import Utils
from tolo_core.view_mixin.jwt_view import JwtAuthViewSet
from tolo_post.serializers.post import PostDetailSerializer
from tolo_post.services.post import PostService


class PostViewSet(JwtAuthViewSet):
    def list(self, request):
        user = request.user
        query_params = Utils.safe_qdict_to_dict(request.query_params)
        posts = PostService.get_posts(user_id=user.id, **query_params)
        return Response(data=posts.get_response(), status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        post = PostService.get_post_detail(pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostDetailSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
