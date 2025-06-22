from django.db import models
from landing_page.models import CreditSimulationLead
from django.utils import timezone

LOAN_PROPOSAL_STATUS = [
    ('0001', 'Criada'), ('0002', 'Enviada'), ('0003', 'Aceita'), ('0004', 'Recusada'), ('0005', 'Expirada'),
    ('0006', 'Cancelada'), ('0007', 'Conferência'), ('0008', 'Enviada para pagamento'), ('0009', 'Paga')
]

PAYMENT_STATUS = [
    ('0001', 'Em dia'), ('0002', 'Quitado'), ('0003', 'Atrasado'), ('0004', 'Inadimplente')
]


class Client(CreditSimulationLead):
    client_since = models.DateField(editable=False, auto_now_add=True, blank=False, null=False, verbose_name="Cliente desde")
    updated = models.DateTimeField(auto_now=True, blank=False, null=False, verbose_name='Data atualizado')
    is_active = models.BooleanField(editable=True, default=True, verbose_name="Cliente ativo")

    def __str__(self):
        return f"Cliente {self.id} - {self.full_name}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class LoanProposal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, editable=False, blank=False, null=False, related_name='loan_proposals', verbose_name="Cliente")
    status = models.CharField(editable=True, max_length=4, blank=False, null=False, choices=LOAN_PROPOSAL_STATUS, verbose_name="Status")
    payment_status = models.CharField(editable=True, max_length=4, blank=False, null=False, choices=PAYMENT_STATUS, verbose_name="Status de pagamento")
    released_value = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor liberado")
    number_of_installments = models.PositiveSmallIntegerField(editable=False, blank=False, null=False, verbose_name="Quantidade de parcelas")
    value_of_installments = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor das parcelas")

    def __str__(self):
        return f"Proposta {self.id} - {self.client.full_name}"

    class Meta:
        verbose_name = "Proposta de empréstimo"
        verbose_name_plural = "Propostas de empréstimo"


class Installment(models.Model):
    loan_proposal = models.ForeignKey(LoanProposal, on_delete=models.CASCADE, editable=False, blank=False, null=False, related_name='installments', verbose_name="Proposta de empréstimo")
    installment_number = models.PositiveSmallIntegerField(editable=False, blank=False, null=False, verbose_name="Número da parcela")
    due_date = models.DateField(editable=False, blank=False, null=False, verbose_name="Data de vencimento")
    payment_date = models.DateField(editable=True, null=True, blank=True, verbose_name="Data de pagamento")
    amount = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor")
    is_paid = models.BooleanField(editable=True, default=False, verbose_name="Pago")

    def is_overdue(self):
        return not self.is_paid and self.due_date < timezone.now().date()

    def __str__(self):
        return f"Parcela {self.installment_number} da proposta {self.loan_proposal.id}"
    
    class Meta:
        verbose_name = "Parcelamento"
        verbose_name_plural = "Parcelamentos"
