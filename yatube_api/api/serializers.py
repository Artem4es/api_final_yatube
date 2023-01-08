from django.db import models
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')
    following = serializers.StringRelatedField(
        source='following.username',
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow


class FollowingField(serializers.Field):
    def to_representation(self, value):
        return value.username

    def to_internal_value(self, data):
        try:
            data = User.objects.get(username=data)
        except User.DoesNotExist:  # такую ошибку не показывает
            raise serializers.ValidationError('Такого юзера нет')
        return data


class FollowPostSerializer(
    serializers.ModelSerializer
):  # может описать модель Follower?
    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.CharField()

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого автора!',
            ),
        ]

    def validate_following(self, following):  # для charfield строка
        current_user = self.context.get('request').user.username
        if following == current_user:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return following
