from django.db import models
from crm_financeiro.models import EncryptedPerson
from django.utils.text import slugify
import hashlib


class CreditSimulationLead(EncryptedPerson):
    cpf_hash = models.CharField(max_length=64, unique=True, editable=False, blank=False, null=False, verbose_name="Hash do CPF")
    slug = slug = models.SlugField(unique=True, max_length=128, editable=False, blank=True, null=False, verbose_name="Slug")
    released_value = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor liberado")
    number_of_installments = models.PositiveSmallIntegerField(editable=False, blank=False, null=False, verbose_name="Quantidade de parcelas")
    value_of_installments = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor das parcelas")
    api_status = models.PositiveSmallIntegerField(editable=False, blank=False, null=False, verbose_name="Status da API")
    created_at = models.DateTimeField(editable=False, auto_now_add=True, blank=False, null=False, verbose_name='Data Criado')

    def __str__(self):
        return f"Simulação - {self.id}"
    
    def save(self, *args, **kwargs):
        if self.cpf:
            self.cpf_hash = hashlib.sha256(self.cpf.encode()).hexdigest()
        
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.slug:
            self.slug = slugify(f"{self.cpf_hash}-{self.created_at}")
            super().save(update_fields=["slug"])


    class Meta:
        verbose_name = "Lead de Simulação de Crédito"
        verbose_name_plural = "Leads de Simulação de Crédito"
