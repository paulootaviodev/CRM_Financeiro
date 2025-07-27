def get_decrypted_matches(search, queryset, related_field=None):
    """
    Use the iterator to search for the search term in encrypted fields
    in the database without overloading memory.
    """
    matched_ids = []

    for obj in queryset.iterator(chunk_size=128):
        try:
            client_obj = getattr(obj, related_field) if related_field else obj
            fields = [
                client_obj.full_name,
                client_obj.cpf,
                client_obj.phone,
                client_obj.email,
                client_obj.city,
            ]

            if any(search.lower() in (field or '').lower() for field in fields):
                matched_ids.append(obj.pk)
        except Exception:
            continue

    return queryset.filter(pk__in=matched_ids)

def encrypted_search(params, queryset, related_field=None):
    """
    Performs a complete database search based on the fields entered in the form.
    Searches for encrypted and unencrypted fields without overloading memory.
    """
    # Search bar
    search = params.get('search')
    if search:
        queryset = get_decrypted_matches(search, queryset, related_field)

    # Filters
    filter_map = {
        # Client filters
        'state': params.get('state') or None,
        'marital_status': params.get('marital_status') or None,
        'employment_status': params.get('employment_status') or None,
        'is_active': params.get('is_active') == 'true' if params.get('is_active') else None,
        'marked_for_deletion': params.get('marked_for_deletion') == 'true' if params.get('marked_for_deletion') else None,
        
        # Loan proposal filters
        'status': params.get('status') or None,
        'payment_status': params.get('payment_status') or None,
    }

    filters = {key: value for key, value in filter_map.items() if value is not None}

    # Range fields
    range_fields = {
        # Client range fields
        'birth_date': (params.get('birth_date_initial'), params.get('birth_date_final')),
        'client_since': (params.get('client_since_initial'), params.get('client_since_final')),
        'created_at': (params.get('created_at_initial'), params.get('created_at_final')),
    
        # Loan proposal range fields
        'released_value': (params.get('released_value_min'), params.get('released_value_max')),
        'number_of_installments': (params.get('number_of_installments_min'), params.get('number_of_installments_max')),
        'value_of_installments': (params.get('value_of_installments_min'), params.get('value_of_installments_max')),
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
