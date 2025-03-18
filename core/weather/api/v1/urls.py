from django.urls import path
from .views import *

urlpatterns = [
    path('',WeatherView.as_view(),name='new'),
    path('api/',WeatherApiView.as_view(),name='weather-api'),
]