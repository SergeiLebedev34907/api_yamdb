from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import PasswordField, RefreshToken
from rest_framework_simplejwt.settings import api_settings

from .validators import NotMeValidator, NoUserValidator

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")
        validators = (NotMeValidator(),)


class AdminUserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        validators = (NotMeValidator(),)


class DestroyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = None


class ChangingUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        "no_active_account": _(
            "No active account found with the given credentials"
        )
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise ValidationError()

        data = {}

        refresh = RefreshToken.for_user(self.user)
        data["token"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    class Meta:
        validators = (NoUserValidator(),)
