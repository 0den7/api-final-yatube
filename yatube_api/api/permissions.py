from rest_framework import permissions


class IsAuthenticatedOrAuthorOrReadOnly(permissions.BasePermission):
    """Кастомный класс пермишенов."""
    def has_permission(self, request, view):
        """Проверяет пермишены на уровне запроса (возможность чтения для
        анонимов, остальные действия только для залогиненных пользователей).
        """
        return (request.method in permissions.SAFE_METHODS
                or (request.user and request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        """
        Проверяет пермишены на уровне конкретного объекта (возможность
        чтения для анонимов, возможность редактирования/удаления только
        для автора).
        """
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author)
