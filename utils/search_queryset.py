from django_eose import search_queryset

def search(params, queryset, related_field=None):
    """
    Performs a complete database search based on the fields entered in the form.
    Searches for encrypted and unencrypted fields without overloading memory.
    """
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

        # Installment filters
        'is_paid': params.get('is_paid') == 'true' if params.get('is_paid') else None,
        'is_canceled': params.get('is_canceled')  == 'true' if params.get('is_canceled') else None
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
    
        # Installment range fields
        'due_date': (params.get('due_date_initial'), params.get('due_date_final')),
        'payment_date': (params.get('payment_date_initial'), params.get('payment_date_final')),
        'amount': (params.get('amount_min'), params.get('amount_max')),
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
        queryset = search_queryset(
            search=search,
            queryset=queryset,
            related_field=related_field,
            fields=("_encrypted_full_name",
                    "_encrypted_cpf",
                    "_encrypted_phone",
                    "_encrypted_email",
                    "city"),
            executor='processes',
            max_batch_size=1_000_000,
            decrypt=True
        )

    return queryset.order_by('-id')
