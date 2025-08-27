from os import getenv

import base64
import hashlib

from django.db import models
from cryptography.fernet import Fernet
from utils.field_kwargs import NON_EDITABLE_FIELD_KWARGS, EDITABLE_FIELD_KWARGS
from utils.field_choices import (
    STATE_CHOICES,
    EMPLOYMENT_STATUS,
    MARITAL_STATUS
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
