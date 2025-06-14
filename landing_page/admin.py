import csv
from django.contrib import admin
from .models import CreditSimulationLead
from django.http import HttpResponse
from django.utils.timezone import now

class CreditSimulationLeadAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'cpf', 'city', 'state', 'marital_status', 'birth_date', 'employment_status',
        'phone', 'email', 'released_value', 'number_of_installments', 'value_of_installments',
        'privacy_policy', 'api_status', 'created_at', 'updated_at'
    )
    list_display_links = ('id', 'full_name', 'cpf', 'phone', 'email')
    search_fields = ('city',)
    list_filter = (
        'state', 'marital_status', 'birth_date', 'employment_status', 'released_value',
        'number_of_installments', 'value_of_installments', 'privacy_policy',
        'api_status', 'created_at'
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'id', 'full_name', 'cpf', 'city', 'state', 'marital_status', 'birth_date', 'employment_status',
        'phone', 'email', 'released_value', 'number_of_installments', 'value_of_installments',
        'privacy_policy', 'api_status', 'created_at', 'updated_at'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_search_results(self, request, queryset, search_term):
        """Searches for both encrypted and unencrypted fields."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            decrypted_matches = CreditSimulationLead.objects.none()

            for obj in CreditSimulationLead.objects.iterator(chunk_size=128):
                try:
                    fields = [obj.full_name, obj.cpf, obj.phone, obj.email]
                    if any(search_term.lower() in field.lower() for field in fields):
                        decrypted_matches |= CreditSimulationLead.objects.filter(pk=obj.pk)
                except Exception:
                    continue  # Ignore decryption errors for invalid records

            # Combines normal and decrypted search results
            queryset |= decrypted_matches

        return queryset, use_distinct

    def export_as_csv(self, request, queryset):
        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Credit_Simulation_Leads_{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                'id', 'full_name', 'cpf', 'city', 'state', 'marital_status', 'birth_date', 'employment_status',
                'phone', 'email', 'released_value', 'number_of_installments', 'value_of_installments',
                'privacy_policy', 'api_status', 'created_at', 'updated_at'
            ]
        )  # CSV Headers

        for simulation in queryset.iterator(chunk_size=128):
            writer.writerow([
                simulation.id,
                simulation.full_name,
                simulation.cpf,
                simulation.city,
                simulation.get_state_display(),
                simulation.get_marital_status_display(),
                simulation.birth_date,
                simulation.get_employment_status_display(),
                simulation.phone,
                simulation.email,
                simulation.released_value,
                simulation.number_of_installments,
                simulation.value_of_installments,
                simulation.privacy_policy,
                simulation.api_status,
                simulation.created_at,
                simulation.updated_at,
            ])

        return response

    export_as_csv.short_description = "Exportar como CSV"

    # Add the action in Django Admin
    actions = [export_as_csv]

admin.site.register(CreditSimulationLead, CreditSimulationLeadAdmin)
admin.site.site_header = "Administração"
admin.site.site_title = "Administração"
admin.site.index_title = "Bem-vindo(a) à página administrativa"
