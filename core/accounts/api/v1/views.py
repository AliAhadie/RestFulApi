from .serializers import (
    RegisterTokenSerializer,
    AuthTokenLoginSerializer,
    ChangePasswordSerializer,
    ProfileApiSerializer,
)
from rest_framework import mixins, generics
from rest_framework.response import Response
from accounts.models import User, Profile
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage,send_mail
from ..utils import SendEmailThread


""" Register User """


class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterTokenSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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

    def get_queryset(self):
        return Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset.filter(user=self.request.user))
        return obj


class SendEmail(generics.GenericAPIView):
    
       def get(self, request, *args, **kwargs):
            message = EmailMessage('email/hello.tpl',{'name':'ali'}, from_email='admin@admin.com',
                                   to=['ali@gmail.com'])
            # TODO: Add more useful commands here.
            SendEmailThread(message).start()
            return Response('email sent')
