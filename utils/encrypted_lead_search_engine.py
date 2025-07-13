def get_decrypted_matches(search, model):
    matches = model.objects.none()
    model_items = model.objects.order_by('-id')

    for obj in model_items.iterator(chunk_size=128):
        try:
            fields = [obj.full_name, obj.cpf, obj.phone, obj.email, obj.city]
            if any(search.lower() in (field or '').lower() for field in fields):
                matches |= model_items.filter(pk=obj.pk)
        except Exception:
            continue

    return matches

def encrypted_search(params, queryset, model):
    search = params.get('search')
    if search:
        queryset = get_decrypted_matches(search, model)

    filter_map = {
        'state': params.get('state') or None,
        'marital_status': params.get('marital_status') or None,
        'employment_status': params.get('employment_status') or None,
        'is_active': params.get('is_active') == 'true' if params.get('is_active') else None,
        'marked_for_deletion': params.get('marked_for_deletion') == 'true' if params.get('marked_for_deletion') else None,
    }

    filters = {key: value for key, value in filter_map.items() if value is not None}

    range_fields = {
        'birth_date': (params.get('birth_date_initial'), params.get('birth_date_final')),
        'client_since': (params.get('client_since_initial'), params.get('client_since_final')),
        'created_at': (params.get('created_at_initial'), params.get('created_at_final')),
    }

    for field, (start, end) in range_fields.items():
        if start and end:
            filters[f'{field}__range'] = [start, end]
        elif start:
            filters[f'{field}__gte'] = start
        elif end:
            filters[f'{field}__lte'] = end

    queryset = queryset.filter(**filters)

    return queryset
