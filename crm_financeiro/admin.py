from django.contrib import admin
from .models import Client, LoanProposal, Installment
from django.http import HttpResponse
from django.utils.timezone import now
import csv


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'cpf', 'city', 'state', 'marital_status', 'birth_date', 'employment_status',
        'phone', 'email', 'client_since', 'updated', 'is_active'
    )
    list_display_links = ('id', 'full_name', 'cpf', 'phone', 'email')
    search_fields = ('city',)
    list_filter = (
        'state', 'marital_status', 'birth_date', 'employment_status', 'released_value',
        'client_since', 'updated', 'is_active'
    )
    ordering = ('-client_since',)
    readonly_fields = (
        'id', 'full_name', 'cpf', 'birth_date', 'released_value', 'number_of_installments',
        'value_of_installments', 'privacy_policy', 'api_status', 'created_at', 'updated_at',
        'client_since', 'updated'
    )

    def has_add_permission(self, request):
        return False

    def get_search_results(self, request, queryset, search_term):
        """Searches for both encrypted and unencrypted fields."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            decrypted_matches = Client.objects.none()

            for obj in Client.objects.iterator(chunk_size=128):
                try:
                    fields = [obj.full_name, obj.cpf, obj.phone, obj.email]
                    if any(search_term.lower() in field.lower() for field in fields):
                        decrypted_matches |= Client.objects.filter(pk=obj.pk)
                except Exception:
                    continue  # Ignore decryption errors for invalid records

            # Combines normal and decrypted search results
            queryset |= decrypted_matches

        return queryset, use_distinct

    def export_as_csv(self, request, queryset):
        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Clients_{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                'id', 'full_name', 'cpf', 'city', 'state', 'marital_status', 'birth_date', 'employment_status',
                'phone', 'email', 'released_value', 'number_of_installments', 'value_of_installments',
                'privacy_policy', 'api_status', 'created_at', 'updated_at', 'client_since', 'updated',
                'is_active'
            ]
        )  # CSV Headers

        for client in queryset.iterator(chunk_size=128):
            writer.writerow([
                client.id,
                client.full_name,
                client.cpf,
                client.city,
                client.get_state_display(),
                client.get_marital_status_display(),
                client.birth_date,
                client.get_employment_status_display(),
                client.phone,
                client.email,
                client.released_value,
                client.number_of_installments,
                client.value_of_installments,
                client.privacy_policy,
                client.api_status,
                client.created_at,
                client.updated_at,
                client.client_since,
                client.updated,
                client.is_active
            ])

        return response

    export_as_csv.short_description = "Exportar como CSV"

    # Add the action in Django Admin
    actions = [export_as_csv]


class LoanProposalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'client', 'status', 'payment_status', 'released_value',
        'number_of_installments', 'value_of_installments',
    )
    list_display_links = ('id', 'client', 'status')
    list_filter = (
        'status', 'payment_status', 'released_value', 'number_of_installments',
        'value_of_installments'
    )
    ordering = ('-id',)
    readonly_fields = (
        'id', 'client', 'payment_status', 'released_value',
        'number_of_installments', 'value_of_installments'
    )

    def has_add_permission(self, request):
        return False

    def get_search_results(self, request, queryset, search_term):
        """Searches for both encrypted and unencrypted fields."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            decrypted_matches = Client.objects.none()

            for obj in Client.objects.iterator(chunk_size=128):
                try:
                    fields = [obj.full_name, obj.cpf, obj.phone, obj.email]
                    if any(search_term.lower() in field.lower() for field in fields):
                        decrypted_matches |= Client.objects.filter(pk=obj.pk)
                except Exception:
                    continue  # Ignore decryption errors for invalid records

            # Combines normal and decrypted search results
            queryset |= decrypted_matches

        return queryset, use_distinct


class InstallmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'loan_proposal', 'installment_number', 'due_date', 'payment_date',
        'amount', 'is_paid'
    )
    list_display_links = ('id', 'loan_proposal')
    list_filter = (
        'installment_number', 'due_date', 'payment_date',
        'amount', 'is_paid'
    )
    ordering = ('-id',)
    readonly_fields = (
        'id', 'loan_proposal', 'installment_number', 'due_date', 'payment_date',
        'amount', 'is_paid'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_search_results(self, request, queryset, search_term):
        """Searches for both encrypted and unencrypted fields."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            decrypted_matches = Client.objects.none()

            for obj in Client.objects.iterator(chunk_size=128):
                try:
                    fields = [obj.full_name, obj.cpf, obj.phone, obj.email]
                    if any(search_term.lower() in field.lower() for field in fields):
                        decrypted_matches |= Client.objects.filter(pk=obj.pk)
                except Exception:
                    continue  # Ignore decryption errors for invalid records

            # Combines normal and decrypted search results
            queryset |= decrypted_matches

        return queryset, use_distinct


admin.site.register(Client, ClientAdmin)
admin.site.register(LoanProposal, LoanProposalAdmin)
admin.site.register(Installment, InstallmentAdmin)
