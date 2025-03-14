from rest_framework import serializers
from accounts.models import User, Profile
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _



class RegisterTokenSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            return serializers.ValidationError("passwords dosnt match")

        errors = {}
        try:
            validators.validate_password(
                password=attrs["password"], user=attrs["email"]
            )

        except serializers.ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(RegisterTokenSerializer, self).validate(attrs)

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return super().create(validated_data)


class AuthTokenLoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), 
                email=email, 
                password=password
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            return serializers.ValidationError("passwords dosnt match")

        errors = {}
        try:
            validators.validate_password(password=attrs["new_password"])

        except serializers.ValidationError as e:
            errors["new_password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(ChangePasswordSerializer, self).validate(attrs)


class ProfileApiSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ("email", "first_name", "last_name", "bio", "image")
        read_only_fields = [
            "email",
        ]


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            return serializers.ValidationError("passwords dosnt match")
        errors = {}
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)
