from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import PostSerializer, CategorySerializer
from blog.models import Post, Category
from rest_framework import status
from .permission import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .paginations import *
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator



class PostListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"category": ["exact", "in"]}
    search_fields = [
        "title",
    ]
    pagination_class = DefaultPaginator

    def perform_create(self, serializer):
        profile = (
            self.request.user.profile
        )  # Assuming the User model has a related Profile model
        serializer.save(author=profile)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"

class PostList(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    template_name = "blog/api-post.html"
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPaginator

class TemplateView(TemplateView) :

    template_name = "blog/api-post.html"
    @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
 



