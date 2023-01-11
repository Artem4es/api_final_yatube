from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
)

from api.custom_viewsets import CreateReadModelViewSet
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
    PostSerializer,
)
from posts.models import Comment, Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post=post_id).select_related(
            'author'
        )
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(
            author=self.request.user, post=Post.objects.get(id=post_id)
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class FollowViewSet(CreateReadModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')
    serializer_class = FollowSerializer

    def get_queryset(self):
        actual_user = self.request.user
        new_queryset = Follow.objects.filter(user=actual_user).select_related(
            'user', 'following'
        )
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )
