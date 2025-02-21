from django.urls import path
from . import views

app_name='api-v1'
urlpatterns = [
    path('post/', views.postlist, name='post-list'),
    path('post/<int:pk>',views.postdetail,name='test')
   
]