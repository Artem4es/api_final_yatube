# TODO:  Напишите свой вариант
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, viewsets, pagination, status
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from posts.models import Comment, Follow, Group, Post, User
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )  # можно в один объёдинить два?
    pagination_class = (
        LimitOffsetPagination  # если есть offset то с ним а так без
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(
            author=self.request.user, post=Post.objects.get(id=post_id)
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class FollowViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')
    serializer_class = FollowSerializer

    def get_queryset(self):
        actual_user = self.request.user
        new_queryset = Follow.objects.filter(user=actual_user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )
