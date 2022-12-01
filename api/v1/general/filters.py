from rest_framework.filters import BaseFilterBackend


class ActiveAndNotDeletedObjectFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_active=True, is_deleted=False)


class ActiveObjectFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_active=True)


class NotDeletedObjectFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_deleted=False)
