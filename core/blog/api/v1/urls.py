from django.urls import path
from . import views
from rest_framework import routers

app_name='api-v1'

routers=routers.DefaultRouter()
routers.register('posts',views.PostListViewSet,basename='post')
routers.register('category',views.CategoryViewSet,basename='category')
urlpatterns = routers.urls

