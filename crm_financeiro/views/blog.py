from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from blog.forms import BlogPostForm
from blog.models import BlogPost
from ..forms import BlogPostFilterForm
from utils.blog_search import blog_search


class CreateBlogPost(LoginRequiredMixin, CreateView):
    template_name = "crm_financeiro/create_blog_post.html"
    model = BlogPost
    form_class = BlogPostForm

    def get_success_url(self):
        messages.success(self.request, "Postagem criada com sucesso.")
        return reverse("update_blog_post", kwargs={"slug": self.object.slug})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('blog.add_blogpost'):
            raise PermissionDenied("Você não tem permissão para criar postagens.")
        return super().dispatch(request, *args, **kwargs)


class ListBlogPosts(LoginRequiredMixin, ListView):
    template_name = "crm_financeiro/list_blog_posts.html"
    context_object_name = "blog_posts"
    model = BlogPost
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BlogPostFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        search_params = self.request.GET

        # Check if any search parameter is present
        if search_params:
            base_queryset = super().get_queryset()
            return blog_search(search_params, base_queryset)
        
        # Return empty queryset if no search input
        return self.model.objects.none()
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('blog.view_blogpost'):
            raise PermissionDenied("Você não tem permissão para visualizar postagens.")
        return super().dispatch(request, *args, **kwargs)


class EditBlogPost(LoginRequiredMixin, UpdateView):
    template_name = "crm_financeiro/update_blog_post.html"
    context_object_name = "blog_post"
    model = BlogPost
    form_class = BlogPostForm
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        messages.success(self.request, "Postagem editada com sucesso.")
        return reverse("update_blog_post", kwargs={"slug": self.object.slug})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('blog.change_blogpost'):
            raise PermissionDenied("Você não tem permissão para editar postagens.")
        return super().dispatch(request, *args, **kwargs)
