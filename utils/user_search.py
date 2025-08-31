from django.db.models import Q

def user_search(params, queryset):
    """
    Performs a complete database search based on the fields entered in the form.
    """
    # Filters
    filter_map = {
        'is_active': params.get('is_active') == 'true' if params.get('is_active') else None,
        'is_staff': params.get('is_staff') == 'true' if params.get('is_staff') else None,
        'is_superuser': params.get('is_superuser') == 'true' if params.get('is_superuser') else None
    }

    filters = {key: value for key, value in filter_map.items() if value is not None}

    # Range fields
    range_fields = {
        # Client range fields
        'date_joined': (params.get('date_joined_initial'), params.get('date_joined_final'))
    }

    for field, (start, end) in range_fields.items():
        if start and end:
            filters[f'{field}__range'] = [start, end]
        elif start:
            filters[f'{field}__gte'] = start
        elif end:
            filters[f'{field}__lte'] = end

    queryset = queryset.filter(**filters)

    # Search bar
    search = params.get('search')
    if search:
        queryset = queryset.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    return queryset.order_by("-id")
