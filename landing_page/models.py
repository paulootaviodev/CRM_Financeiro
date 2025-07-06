from django.db import models
from crm_financeiro.models import EncryptedPerson


class CreditSimulationLead(EncryptedPerson):
    released_value = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor liberado")
    number_of_installments = models.PositiveSmallIntegerField(editable=False, blank=False, null=False, verbose_name="Quantidade de parcelas")
    value_of_installments = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor das parcelas")
    api_status = models.PositiveSmallIntegerField(editable=False, blank=False, null=False, verbose_name="Status da API")
    created_at = models.DateTimeField(editable=False, auto_now_add=True, blank=False, null=False, verbose_name='Data Criado')

    def __str__(self):
        return f"Simulação - {self.id}"

    class Meta:
        verbose_name = "Lead de Simulação de Crédito"
        verbose_name_plural = "Leads de Simulação de Crédito"
