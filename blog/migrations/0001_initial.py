# Generated by Django 5.2 on 2025-06-21 18:25

import django_summernote.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Título')),
                ('short_description', models.CharField(max_length=128, verbose_name='Descrição curta')),
                ('featured_image', models.ImageField(upload_to='blog_posts/', verbose_name='Imagem destacada')),
                ('content', django_summernote.fields.SummernoteTextField(max_length=20000, verbose_name='Conteúdo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data Criado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data Atualizado')),
            ],
            options={
                'verbose_name': 'Postagem do blog',
                'verbose_name_plural': 'Postagens do blog',
            },
        ),
    ]
