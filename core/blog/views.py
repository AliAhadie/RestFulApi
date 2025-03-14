from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    RedirectView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.list import ListView
from blog.models import Post
from django.core.exceptions import ImproperlyConfigured
from blog.forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


"""view with templateview"""


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "REST API"
        return context


"""view with redirectview"""


class RedirectToUi(RedirectView):
    url = "https://ui.ac.ir/"


"""view for listview"""


class PostView(LoginRequiredMixin, ListView):
    model = Post
    queryset = Post.objects.all()
    paginate_by = 2
    context_object_name = "posts"


"""show detail of post"""


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"


"""create object for post with form if user is authenticated"""


class PostFormView(CreateView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/blog/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    template_name = "contact.html"
    model = Post
    form_class = ContactForm
    success_url = "/blog/"


class PostDeleteView(DeleteView):
    success_url = "/blog/"
    model = Post
