from django.db import models
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


class CreditSimulationLead(models.Model):
    _encrypted_full_name = models.BinaryField(editable=False, blank=False, null=False, verbose_name="Nome completo")
    _encrypted_cpf = models.BinaryField(editable=False, blank=False, null=False, verbose_name="CPF")
    city = models.CharField(editable=False, max_length=128, blank=False, null=False, verbose_name="Cidade")
    state = models.CharField(editable=False, max_length=2, blank=False, null=False, choices=STATE_CHOICES, verbose_name="Estado")
    marital_status = models.CharField(editable=False, max_length=1, blank=False, null=False, choices=MARITAL_STATUS, verbose_name="Estado Civil")
    birth_date = models.DateField(editable=False, blank=False, null=False, verbose_name="Data de Nascimento")
    employment_status = models.CharField(editable=False, max_length=1, blank=False, null=False, choices=EMPLOYMENT_STATUS , verbose_name="Situação Empregatícia")
    _encrypted_phone = models.BinaryField(editable=False, blank=False, null=False, verbose_name="Telefone")
    _encrypted_email = models.BinaryField(editable=False, blank=False, null=False, verbose_name="E-mail")
    released_value = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor liberado")
    number_of_installments = models.PositiveSmallIntegerField(editable=False, blank=False, null=False, verbose_name="Quantidade de parcelas")
    value_of_installments = models.DecimalField(editable=False, max_digits=14, decimal_places=2, blank=False, null=False, verbose_name="Valor das parcelas")
    privacy_policy = models.BooleanField(editable=False, blank=False, null=False, verbose_name="Política de Privacidade")
    api_status = models.PositiveSmallIntegerField(editable=False, blank=False, null=False, verbose_name="Status da API")
    created_at = models.DateTimeField(editable=False, auto_now_add=True, blank=False, null=False, verbose_name='Data Criado')
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False, verbose_name='Data Atualizado')

    def __str__(self):
        return f'Simulação - {self.id}'

    def _decrypt_field(self, encrypted_value):
        f = Fernet(AES_KEY)
        return f.decrypt(encrypted_value).decode()
    
    def _encrypt_field(self, value):
        f = Fernet(AES_KEY)
        return f.encrypt(value.encode())
    
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

    class Meta:
        verbose_name = "Lead de Simulação de Crédito"
        verbose_name_plural = "Leads de Simulação de Crédito"
