from django.urls import path
from crm_financeiro.views import (
    CreateBlogPost,
    EditBlogPost,
    ListBlogPosts
)

urlpatterns = [
    path("criar-postagem/", CreateBlogPost.as_view(), name="create_blog_post"),
    path("listar-postagens/", ListBlogPosts.as_view(), name="list_blog_posts"),
    path("editar-postagem/<slug:slug>/", EditBlogPost.as_view(), name="update_blog_post")
]
