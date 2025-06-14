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
    search_fields = ('full_name', 'cpf', 'city', 'phone', 'email')
    list_filter = (
        'state', 'marital_status', 'birth_date', 'employment_status', 'released_value',
        'number_of_installments', 'value_of_installments', 'privacy_policy',
        'api_status', 'created_at'
    )
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_search_results(self, request, queryset, search_term):
        """Searches for both encrypted and unencrypted fields."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            decrypted_matches = CreditSimulationLead.objects.none()
            batch_size = 128
            total_records = CreditSimulationLead.objects.count()

            for batch_start in range(0, total_records, batch_size):
                batch = CreditSimulationLead.objects.all()[batch_start:batch_start + batch_size]
                for obj in batch:
                    try:
                        if search_term.lower() in obj.full_name.lower():
                            decrypted_matches |= CreditSimulationLead.objects.filter(pk=obj.pk)
                        elif search_term.lower() in obj.cpf().lower():
                            decrypted_matches |= CreditSimulationLead.objects.filter(pk=obj.pk)
                        elif search_term.lower() in obj.phone().lower():
                            decrypted_matches |= CreditSimulationLead.objects.filter(pk=obj.pk)
                        elif search_term.lower() in obj.email().lower():
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

        batch_size = 128
        total_records = queryset.count()

        for batch_start in range(0, total_records, batch_size):
            batch = queryset[batch_start:batch_start + batch_size]
            for simulation in batch:
                writer.writerow([
                    simulation.id,
                    simulation.full_name,
                    simulation.cpf,
                    simulation.city,
                    simulation.state,
                    simulation.marital_status,
                    simulation.birth_date,
                    simulation.employment_status,
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
