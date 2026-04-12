from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions, pagination, mixins

from posts.models import Post, Group
from api.serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import IsAuthenticatedOrAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrAuthorOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination
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
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrAuthorOrReadOnly,)

    def get_post(self):
        """Метод возвращает пост по post_id из эндпоинта или HTTP404."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        """Метод возвращает комментарии к отдельному посту."""
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        """
        Метод для автоматического установления автора и поста
        при создании комментария.
        """
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Вьюсет для работы с подписками.
    Поддерживает только GET (получение списка подписок) и POST
    (создание подписки).
    """
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Возвращает только подписки текущего пользователя."""
        return self.request.user.subscriptions.all()
