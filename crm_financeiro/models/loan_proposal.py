from django.db import models
from django.utils.text import slugify
from .client import Client
from utils.field_choices import (
    LOAN_PROPOSAL_STATUS,
    PAYMENT_STATUS
)


class LoanProposal(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='loan_proposals',
        editable=False,
        blank=False,
        null=False,
        verbose_name="Cliente"
    )
    status = models.CharField(
        editable=True,
        blank=False,
        null=False,
        max_length=4,
        choices=LOAN_PROPOSAL_STATUS,
        verbose_name="Status"
    )
    payment_status = models.CharField(
        editable=True,
        blank=False,
        null=False,
        max_length=4,
        choices=PAYMENT_STATUS,
        verbose_name="Status de pagamento"
    )
    released_value = models.DecimalField(
        editable=False,
        blank=False,
        null=False,
        max_digits=14,
        decimal_places=2,
        verbose_name="Valor liberado"
    )
    number_of_installments = models.PositiveSmallIntegerField(
        editable=False,
        blank=False,
        null=False,
        verbose_name="Quantidade de parcelas"
    )
    value_of_installments = models.DecimalField(
        editable=False,
        blank=False,
        null=False,
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
        auto_now=True,
        editable=True,
        blank=False,
        null=False,
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
