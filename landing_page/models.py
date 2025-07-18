import hashlib

from crm_financeiro.models import EncryptedPerson
from django.db import models
from utils.field_kwargs import NON_EDITABLE_FIELD_KWARGS
from django.utils.text import slugify


class CreditSimulationLead(EncryptedPerson):
    cpf_hash = models.CharField(
        **NON_EDITABLE_FIELD_KWARGS,
        max_length=64,
        unique=False,
        verbose_name="Hash do CPF"
    )
    slug = models.SlugField(
        unique=True,
        max_length=128,
        editable=False,
        blank=True,
        null=False,
        verbose_name="Slug"
    )
    released_value = models.DecimalField(
        **NON_EDITABLE_FIELD_KWARGS,
        max_digits=14,
        decimal_places=2,
        verbose_name="Valor liberado"
    )
    number_of_installments = models.PositiveSmallIntegerField(
        **NON_EDITABLE_FIELD_KWARGS,
        verbose_name="Quantidade de parcelas"
    )
    value_of_installments = models.DecimalField(
        **NON_EDITABLE_FIELD_KWARGS,
        max_digits=14,
        decimal_places=2,
        verbose_name="Valor das parcelas"
    )
    api_status = models.PositiveSmallIntegerField(
        **NON_EDITABLE_FIELD_KWARGS,
        verbose_name="Status da API"
    )
    created_at = models.DateTimeField(
        **NON_EDITABLE_FIELD_KWARGS,
        auto_now_add=True,
        verbose_name='Data Criado'
    )

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
