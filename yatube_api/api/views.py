from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions, exceptions

from posts.models import Post, Group, Follow
from api.serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadOnly
from .pagination import PostPagination


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = PostPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('pub_date',)
    ordering = ('pub_date',)

    def perform_create(self, serializer):
        """Автоматическое установление автора при создании поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с группами (только для чтения)."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('created',)
    ordering = ('created',)

    def get_queryset(self):
        """
        Метод возвращает кверисет комментариев для отдельного поста из
        post_id из эндпоинта.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        """
        Метод для автоматического установления автора и поста
        при создании комментария.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с подписками."""
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Возвращает только подписки текущего пользователя."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Создает новую подписку с автоматическим установлением автора и
        проверкой на дублирование подписки.
        """
        following = serializer.validated_data['following']
        if Follow.objects.filter(
            user=self.request.user,
            following=following
        ).exists():
            raise exceptions.ValidationError({
                'following': 'Вы уже подписаны на этого пользователя!'
            })
        serializer.save(user=self.request.user)
