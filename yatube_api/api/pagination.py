from rest_framework.pagination import LimitOffsetPagination


class PostPagination(LimitOffsetPagination):
    """Кастомная пагинация для постов."""
    default_limit = None

    def paginate_queryset(self, queryset, request, view):
        """
        Применяет пагинацию к queryset только при наличии параметров запроса
        'limit' или 'offset'.
        Если параметры отсутствуют, возвращается полный список постов
        без пагинации.
        """
        if ('limit' not in request.query_params
                and 'offset' not in request.query_params):
            return None
        return super().paginate_queryset(queryset, request, view)
