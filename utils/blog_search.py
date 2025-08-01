from django.db.models import Q

def blog_search(params, queryset):
    """
    Performs a complete database search based on the fields entered in the form.
    """
    # Search bar
    search = params.get('search')
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(content__icontains=search)
        )

    # Range fields
    range_fields = {
        # Client range fields
        'created_at': (params.get('created_at_initial'), params.get('created_at_final')),
        'updated_at': (params.get('updated_at_initial'), params.get('updated_at_final'))
    }

    filters = dict()

    for field, (start, end) in range_fields.items():
        if start and end:
            filters[f'{field}__range'] = [start, end]
        elif start:
            filters[f'{field}__gte'] = start
        elif end:
            filters[f'{field}__lte'] = end

    queryset = queryset.filter(**filters)

    return queryset
