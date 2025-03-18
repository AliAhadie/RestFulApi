from rest_framework.generics import GenericAPIView,ListAPIView
import requests
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


from rest_framework.response import Response

class WeatherApiView(GenericAPIView):
    @method_decorator(cache_page(2000))
    def get(self,request):
        url = 'http://api.weatherapi.com/v1/current.json?key=618a11e2f4324386965124130251703&q=Tehran&lang=fa'
        response = requests.get(url)
        return Response(response.json())


class WeatherView(TemplateView):
   template_name = 'weather/weather.html'

    
