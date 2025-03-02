from django.urls import include,path
from .views import *
from rest_framework.authtoken.views import ObtainAuthToken

app_name='api-v1'


urlpatterns=[
    #register user
    path('register/',RegisterApiView.as_view(),name='register'),
    path('token/login',CustomAuthToken.as_view(),name='login'),
    path('token/logut/',LogoutApiToken.as_view(),name='logout'),


]