from .serializers import (
    RegisterTokenSerializer,
    AuthTokenLoginSerializer,
    ChangePasswordSerializer,
    ProfileApiSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer
)
from rest_framework import  generics
from rest_framework.response import Response
from accounts.models import User, Profile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ..utils import SendEmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from blog.api.v1.permission import IsVrifed,IsNotAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.hashers import make_password
from blog.tasks import send_email


""" Register User """


class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterTokenSerializer
    permission_classes=[IsNotAuthenticated]

    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token)}
    

    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email=serializer.validated_data['email']
            user=User.objects.get(email=email)
            token=self.get_tokens_for_user(user)
            message = EmailMessage('email/hello.tpl',{'token':token}, from_email='admin@admin.com',
                                   to=[email])
            send_email(message)
            return Response('email sent')
        return Response(serializer.errors)
   



"""login user"""


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


"""logout user"""


class LogoutApiToken(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeUserPasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        obj = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not obj.check_password(serializer.validated_data.get("old_password")):
                return Response("wrong password !", status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(serializer.validated_data.get("new_password"))
            obj.save()
            return Response("password succssefuly change ", status=status.HTTP_200_OK)

        return Response(serializer.errors)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileApiSerializer
    permission_classes=[IsAuthenticated,IsVrifed]

    def get_queryset(self):
        return Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset.filter(user=self.request.user))
        return obj


class SendEmail(generics.GenericAPIView):
    
        def get(self, request, *args, **kwargs):
            user=self.request.user
            token=self.get_tokens_for_user(user)
            message = EmailMessage('email/hello.tpl',{'token':token}, from_email='admin@admin.com',
                                   to=['ali@gmail.com'])
         
            send_email(message)
            return Response('email sent')
      
        def get_tokens_for_user(self,user):
            refresh = RefreshToken.for_user(user)

            return str(refresh.access_token)

class ActivationUser(generics.GenericAPIView):
    def get(self, request,token, *args, **kwargs):
        try:
            token=jwt.decode(token, 'secret', algorithms=['HS256'])
            user=User.objects.get(id=token['user_id'])
            user.is_verified=True
            user.save()
            return Response('user activated')
        except jwt.ExpiredSignatureError:
            return Response('activation link expired')
        except jwt.DecodeError:
            return Response('invalid token')        
        

class ForgetPasswordView(generics.GenericAPIView):

    serializer_class=ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        email=request.data.get('email')
        

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "user not found "}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            
            refresh = RefreshToken.for_user(user)
            reset_token = str(refresh.access_token)
            message = EmailMessage('email/reset_password.tpl',{'token':reset_token}, from_email='admin@admin.com',
                                   to=['ali@gmail.com'])
            SendEmailThread(message).start()
            return Response('reset password send')

         
          
class ChangePassword(generics.GenericAPIView):
    serializer_class=ResetPasswordSerializer
    def post(self, request,token):
        new_password = request.data.get("new_password")

        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token["user_id"]
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response('token is not valid', status=status.HTTP_400_BAD_REQUEST)

        # تغییر رمز عبور کاربر
        user.password = make_password(new_password)
        user.save()

        return Response({"message": "password change successfully"}, status=status.HTTP_200_OK)
                
    