from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from cryptography.fernet import Fernet
from os import getenv
import base64
import hashlib

# AES-256 key generation
AES_PASSWORD = getenv("AES_PASSWORD").encode()
AES_KEY = base64.urlsafe_b64encode(hashlib.sha256(AES_PASSWORD).digest())

STATE_CHOICES = [
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
    ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'),
    ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]

EMPLOYMENT_STATUS  = [
    ('1', 'Funcionário Público'), ('2', 'Assalariado (CLT)'), ('3', 'Autônomo'), ('4', 'Empresário ou PJ'),
    ('5', 'Profissional Liberal'), ('6', 'Aposentado ou Pensionista'), ('7', 'Desempregado'), ('8', 'Programa Bolsa Família')
]

MARITAL_STATUS = [
    ('S', 'Solteiro(a)'), ('C', 'Casado(a)'), ('D', 'Divorciado(a)'), ('V', 'Viúvo(a)')
]

LOAN_PROPOSAL_STATUS = [
    ('0001', 'Gerada'), ('0002', 'Enviada para o cliente'), ('0003', 'Aceita'), ('0004', 'Recusada'), ('0005', 'Expirada'),
    ('0006', 'Cancelada'), ('0007', 'Em conferência'), ('0008', 'Paga na conta do cliente')
]

PAYMENT_STATUS = [
    ('0001', 'Em dia'), ('0002', 'Quitado'), ('0003', 'Atrasado'), ('0004', 'Inadimplente')
]


class EncryptedPerson(models.Model):
    _encrypted_full_name = models.BinaryField(editable=False, blank=False, null=False, verbose_name="Nome completo")
    _encrypted_cpf = models.BinaryField(editable=False, blank=False, null=False, verbose_name="CPF")
    _encrypted_phone = models.BinaryField(editable=True, blank=False, null=False, verbose_name="Telefone")
    _encrypted_email = models.BinaryField(editable=True, blank=False, null=False, verbose_name="E-mail")
    city = models.CharField(editable=True, max_length=128, blank=False, null=False, verbose_name="Cidade")
    state = models.CharField(editable=True, max_length=2, blank=False, null=False, choices=STATE_CHOICES, verbose_name="Estado")
    marital_status = models.CharField(editable=True, max_length=1, blank=False, null=False, choices=MARITAL_STATUS, verbose_name="Estado Civil")
    birth_date = models.DateField(editable=False, blank=False, null=False, verbose_name="Data de Nascimento")
    employment_status = models.CharField(editable=True, max_length=1, blank=False, null=False, choices=EMPLOYMENT_STATUS , verbose_name="Situação Empregatícia")
    privacy_policy = models.BooleanField(editable=False, blank=False, null=False, verbose_name="Política de Privacidade")
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False, verbose_name='Data Atualizado')

    class Meta:
        abstract = True

    def _decrypt_field(self, encrypted_value):
        return Fernet(AES_KEY).decrypt(encrypted_value).decode()

    def _encrypt_field(self, value):
        return Fernet(AES_KEY).encrypt(value.encode())

    @staticmethod
    def _property(field_name):
        def getter(self):
            return self._decrypt_field(getattr(self, field_name))
        def setter(self, value):
            setattr(self, field_name, self._encrypt_field(value))
        return property(getter, setter)

    full_name = _property('_encrypted_full_name')
    cpf = _property('_encrypted_cpf')
    phone = _property('_encrypted_phone')
    email = _property('_encrypted_email')


class Client(EncryptedPerson):
    cpf_hash = models.CharField(max_length=64, unique=True, editable=False, blank=False, null=False, verbose_name="Hash do CPF")
    slug = slug = models.SlugField(unique=True, max_length=128, editable=False, blank=True, null=False, verbose_name="Slug")
    is_active = models.BooleanField(default=True, verbose_name="Cliente ativo")
    client_since = models.DateTimeField(auto_now_add=True, verbose_name='Cliente Desde')

    def __str__(self):
        return f"Cliente {self.id} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        if self.cpf:
            self.cpf_hash = hashlib.sha256(self.cpf.encode()).hexdigest()
        
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.slug:
            self.slug = slugify(f"{self.cpf_hash}-{self.client_since}")
            super().save(update_fields=["slug"])

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
