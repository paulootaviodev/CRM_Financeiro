import hashlib

from django.db import models
from django.utils.text import slugify
from utils.field_kwargs import NON_EDITABLE_FIELD_KWARGS
from .encrypted_person import EncryptedPerson


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
    slug = models.SlugField(
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
            self.slug = slugify(f"{self.pk}{self.cpf_hash}-{self.client_since}")
            super().save(update_fields=["slug"])

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
