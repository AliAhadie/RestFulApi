from django.urls import include,path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name='api-v1'


urlpatterns=[
    #register user
    path('register/',RegisterApiView.as_view(),name='register'),
    path('token/login',CustomAuthToken.as_view(),name='login'),
    path('token/logut/',LogoutApiToken.as_view(),name='logout'),
    path('jwt/create/',TokenObtainPairView.as_view(),name='jwt-create'),
    path('jwt/refresh/',TokenRefreshView.as_view(),name='jwt-refresh'),
    path('change-password/',ChangeUserPasswordView.as_view(),name='change-pass'),
    path('user/profile',ProfileApiView.as_view(),name='profile'),
    path('email/',SendEmail.as_view(),name='email')

]