from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from .loan_proposal import LoanProposal
from utils.field_kwargs import NON_EDITABLE_FIELD_KWARGS, EDITABLE_FIELD_KWARGS


class Installment(models.Model):
    loan_proposal = models.ForeignKey(
        LoanProposal,
        **NON_EDITABLE_FIELD_KWARGS,
        on_delete=models.CASCADE,
        related_name='installments',
        verbose_name="Proposta de empréstimo"
    )
    installment_number = models.PositiveSmallIntegerField(
        **NON_EDITABLE_FIELD_KWARGS,
        verbose_name="Número da parcela"
    )
    due_date = models.DateField(
        **NON_EDITABLE_FIELD_KWARGS,
        verbose_name="Data de vencimento"
    )
    payment_date = models.DateField(
        editable=True,
        null=True,
        blank=True,
        verbose_name="Data de pagamento"
    )
    amount = models.DecimalField(
        **NON_EDITABLE_FIELD_KWARGS,
        max_digits=14,
        decimal_places=2,
        verbose_name="Valor"
    )
    is_paid = models.BooleanField(
        editable=True,
        default=False,
        verbose_name="Pago"
    )
    is_canceled = models.BooleanField(
        editable=True,
        default=False,
        verbose_name="Está cancelado"
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

    def is_overdue(self):
        return not self.is_paid and self.due_date < timezone.now().date()

    def __str__(self):
        return f"Parcela {self.installment_number} da proposta {self.loan_proposal.id}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.slug:
            self.slug = slugify(f"{self.loan_proposal.slug}{self.pk}{self.created_at}")
            super().save(update_fields=["slug"])

    
    class Meta:
        verbose_name = "Parcelamento"
        verbose_name_plural = "Parcelamentos"
