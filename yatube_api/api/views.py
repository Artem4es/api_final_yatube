# TODO:  Напишите свой вариант
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework import filters, viewsets, pagination, status
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
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    FollowPostSerializer,
    FollowRetrieveSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )  # можно в один объёдинить два?
    # pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = None
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
    search_fields = ('following',)

    def get_serializer_class(self):
        if self.action == 'create':
            return FollowPostSerializer
        return FollowRetrieveSerializer

    def get_queryset(self):
        actual_user = self.request.user
        new_queryset = Follow.objects.filter(user=actual_user)
        return new_queryset

    def perform_create(self, serializer):
        following_username = serializer.validated_data.get('following')
        try:
            serializer.save(
                user=self.request.user,
                following=User.objects.get(username=following_username),
            )
        except IntegrityError:
            raise ValidationError('Такая подписка уже есть!')
        except User.DoesNotExist:
            raise ValidationError('Нет такого пользователя')
