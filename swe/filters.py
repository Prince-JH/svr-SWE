from rest_framework import filters


class IdsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        param = request.GET.get('ids')
        if not param:
            return queryset
        param = param.replace('(', '')
        param = param.replace(')', '')
        ids = list(param.split(','))
        return queryset.filter(id__in=ids)
