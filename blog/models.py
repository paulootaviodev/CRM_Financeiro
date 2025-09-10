from django.db import models
from utils.resize_image import process_image
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(
        editable=True,
        blank=False,
        null=False,
        max_length=64,
        verbose_name="Título"
    )
    short_description = models.CharField(
        editable=True,
        blank=False,
        null=False,
        max_length=128,
        verbose_name="Descrição curta"
    )
    featured_image = models.ImageField(
        upload_to="blog_posts/",
        editable=True,
        blank=False,
        null=False,
        verbose_name="Imagem destacada"
    )
    content = models.TextField(
        editable=True,
        blank=False,
        null=False,
        max_length=20000,
        verbose_name="Conteúdo"
    )
    slug = models.SlugField(
        unique=True,
        editable=False,
        blank=True,
        null=False,
        verbose_name="Slug"
    )
    views = models.PositiveIntegerField(
        default=0,
        editable=True,
        blank=True,
        null=False,
        verbose_name="Visualizações"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False,
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
        return f"Postagem {self.id} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.featured_image:
            self.featured_image = process_image(self.featured_image)

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.slug:
            self.slug = slugify(f"{self.title}-{self.created_at.strftime('%d-%m-%Y-%S')}{self.pk}")
            super().save(update_fields=["slug"])
    
    class Meta:
        verbose_name = "Postagem do blog"
        verbose_name_plural = "Postagens do blog"


class ViewsPerMonth(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        editable=False,
        blank=False,
        null=False,
        verbose_name="Postagem"
    )
    month = models.DateField(
        editable=False,
        blank=False,
        null=False,
        verbose_name="Mês"
    )
    total = models.PositiveIntegerField(
        default=0,
        editable=True,
        blank=True,
        null=False,
        verbose_name="Total"
    )

    class Meta:
        unique_together = ('post', 'month')
        verbose_name = 'Visualização por mês'
        verbose_name_plural = 'Visualizações por mês'

    def __str__(self):
        return f"{self.post.title} - {self.month.strftime('%m/%Y')}: {self.total}"
