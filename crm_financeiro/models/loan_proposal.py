from django.db import models
from django.utils.text import slugify
from .client import Client
from utils.field_kwargs import NON_EDITABLE_FIELD_KWARGS, EDITABLE_FIELD_KWARGS
from utils.field_choices import (
    LOAN_PROPOSAL_STATUS,
    PAYMENT_STATUS
)


class LoanProposal(models.Model):
    client = models.ForeignKey(
        Client,
        **NON_EDITABLE_FIELD_KWARGS,
        on_delete=models.CASCADE,
        related_name='loan_proposals',
        verbose_name="Cliente"
    )
    status = models.CharField(
        **EDITABLE_FIELD_KWARGS,
        max_length=4,
        choices=LOAN_PROPOSAL_STATUS,
        verbose_name="Status"
    )
    payment_status = models.CharField(
        **EDITABLE_FIELD_KWARGS,
        max_length=4,
        choices=PAYMENT_STATUS,
        verbose_name="Status de pagamento"
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
    slug = models.SlugField(
        unique=True,
        max_length=128,
        editable=False,
        blank=True,
        null=False,
        verbose_name="Slug"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data Criado'
    )
    updated_at = models.DateTimeField(
        **EDITABLE_FIELD_KWARGS,
        auto_now=True,
        verbose_name='Data Atualizado'
    )

    def __str__(self):
        return f"Proposta {self.id} - {self.client.full_name}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.client.cpf_hash and not self.slug:
            self.slug = slugify(f"{self.client.cpf_hash}{self.pk}")
            super().save(update_fields=["slug"])

    class Meta:
        verbose_name = "Proposta de empréstimo"
        verbose_name_plural = "Propostas de empréstimo"
