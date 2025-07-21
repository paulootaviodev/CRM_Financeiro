from os import getenv

import base64
import hashlib

from cryptography.fernet import Fernet
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from utils.field_kwargs import NON_EDITABLE_FIELD_KWARGS, EDITABLE_FIELD_KWARGS
from utils.field_choices import (
    STATE_CHOICES,
    EMPLOYMENT_STATUS,
    MARITAL_STATUS,
    LOAN_PROPOSAL_STATUS,
    PAYMENT_STATUS
)

# AES-256 key generation
AES_PASSWORD = getenv("AES_PASSWORD").encode()
AES_KEY = base64.urlsafe_b64encode(hashlib.sha256(AES_PASSWORD).digest())


class EncryptedPerson(models.Model):
    # Encrypted fields
    _encrypted_full_name = models.BinaryField(
        **NON_EDITABLE_FIELD_KWARGS,
        verbose_name="Nome completo"
    )
    _encrypted_cpf = models.BinaryField(
        **NON_EDITABLE_FIELD_KWARGS,
        verbose_name="CPF"
    )
    _encrypted_phone = models.BinaryField(
        **EDITABLE_FIELD_KWARGS,
        verbose_name="Telefone"
    )
    _encrypted_email = models.BinaryField(
        **EDITABLE_FIELD_KWARGS,
        verbose_name="E-mail"
    )

    # Personal data
    city = models.CharField(
        **EDITABLE_FIELD_KWARGS,
        max_length=128,
        verbose_name="Cidade"
    )
    state = models.CharField(
        **EDITABLE_FIELD_KWARGS,
        max_length=2,
        choices=STATE_CHOICES,
        verbose_name="Estado"
    )
    birth_date = models.DateField(
        **EDITABLE_FIELD_KWARGS,
        verbose_name="Data de Nascimento"
    )
    marital_status = models.CharField(
        **EDITABLE_FIELD_KWARGS,
        max_length=1,
        choices=MARITAL_STATUS,
        verbose_name="Estado Civil"
    )
    employment_status = models.CharField(
        **EDITABLE_FIELD_KWARGS,
        max_length=1,
        choices=EMPLOYMENT_STATUS,
        verbose_name="Situação Empregatícia"
    )
    
    # Metadata
    privacy_policy = models.BooleanField(
        **NON_EDITABLE_FIELD_KWARGS,
        verbose_name="Política de Privacidade"
    )
    updated_at = models.DateTimeField(
        **EDITABLE_FIELD_KWARGS,
        auto_now=True,
        verbose_name='Data Atualizado'
    )

    class Meta:
        abstract = True

    def _decrypt_field(self, encrypted_value):
        return Fernet(AES_KEY).decrypt(encrypted_value).decode()

    def _encrypt_field(self, value):
        return Fernet(AES_KEY).encrypt(value.encode())

    @staticmethod
    def _property(field_name):
        # Getter decrypts the field value before returning it.
        def getter(self):
            return self._decrypt_field(getattr(self, field_name))
        
        # Setter encrypts the value before setting it to the field.
        def setter(self, value):
            setattr(self, field_name, self._encrypt_field(value))

        return property(getter, setter)

    full_name = _property('_encrypted_full_name')
    cpf = _property('_encrypted_cpf')
    phone = _property('_encrypted_phone')
    email = _property('_encrypted_email')


class Client(EncryptedPerson):
    cpf_hash = models.CharField(
        **NON_EDITABLE_FIELD_KWARGS,
        max_length=64,
        unique=True,
        verbose_name="Hash do CPF"
    )
    is_active = models.BooleanField(
        default=True,
        editable=True,
        verbose_name="Cliente ativo"
    )
    client_since = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Cliente Desde'
    )
    marked_for_deletion = models.BooleanField(
        default=False,
        editable=True,
        verbose_name="Marcado para exclusão"
    )
    slug = slug = models.SlugField(
        unique=True,
        max_length=128,
        editable=False,
        blank=True,
        null=False,
        verbose_name="Slug"
    )
    deletion_request_date = models.DateField(
        blank=True,
        null=True,
        editable=True,
        verbose_name="Data de solicitação de exclusão"
    )

    def __str__(self):
        return f"Cliente {self.id} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        if self.cpf:
            self.cpf_hash = hashlib.sha256(self.cpf.encode()).hexdigest()

        if self.is_active and self.marked_for_deletion:
            raise ValueError("Um cliente ativo não pode estar marcado para exclusão.")
        
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.slug:
            self.slug = slugify(f"{self.cpf_hash}-{self.client_since}")
            super().save(update_fields=["slug"])

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


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

    def __str__(self):
        return f"Proposta {self.id} - {self.client.full_name}"

    class Meta:
        verbose_name = "Proposta de empréstimo"
        verbose_name_plural = "Propostas de empréstimo"


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

    def is_overdue(self):
        return not self.is_paid and self.due_date < timezone.now().date()

    def __str__(self):
        return f"Parcela {self.installment_number} da proposta {self.loan_proposal.id}"
    
    class Meta:
        verbose_name = "Parcelamento"
        verbose_name_plural = "Parcelamentos"
