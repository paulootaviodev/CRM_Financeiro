from django.db import models
from django.utils.text import slugify
from utils.resize_image import process_image # type: ignore


class BlogPost(models.Model):
    title = models.CharField(editable=True, max_length=64, blank=False, null=False, verbose_name="Título")
    short_description = models.CharField(editable=True, max_length=128, blank=False, null=False, verbose_name="Descrição curta")
    featured_image = models.ImageField(upload_to="blog_posts/", editable=True, blank=False, null=False, verbose_name="Imagem destacada")
    content = models.TextField(editable=True, max_length=20000, blank=False, null=False, verbose_name="Conteúdo")
    slug = models.SlugField(unique=True, editable=False, blank=True, null=False, verbose_name="Slug")
    created_at = models.DateTimeField(editable=False, auto_now_add=True, blank=False, null=False, verbose_name='Data Criado')
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False, verbose_name='Data Atualizado')

    def __str__(self):
        return f"Postagem {self.id} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.featured_image:
            self.featured_image = process_image(self.featured_image)

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.slug:
            self.slug = slugify(f"{self.title}-{self.created_at.strftime("%d-%m-%Y-%S")}")
            super().save(update_fields=["slug"])
    
    class Meta:
        verbose_name = "Postagem do blog"
        verbose_name_plural = "Postagens do blog"
