
from .serializers import RegisterTokenSerializer,AuthTokenLoginSerializer
from rest_framework import mixins,generics
from rest_framework.response import Response
from accounts.models import User
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status

""" Register User """
class RegisterApiView(generics.CreateAPIView):
    serializer_class=RegisterTokenSerializer

    def post (self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

"""login user"""
class CustomAuthToken(ObtainAuthToken):
    serializer_class=AuthTokenLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

"""logout user"""
class LogoutApiToken(APIView):
    def post(self,request):
        request.user.auth_token.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)

    








    


        


    
