import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from .pagination import PageNumberPagination5
from .permissions import IsAdmin
from .serializers import (
    AdminUserManagementSerializer,
    ChangingUserDataSerializer,
    CustomTokenObtainPairSerializer,
    DestroyUserSerializer,
    UserSignUpSerializer,
)

User = get_user_model()


def create_password(length=25):
    symbols = (
        "!", "#", "$", "%", "&", "(", ")", "*", "+", ",", "-", ".", "/", "2",
        "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@",
        "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P",
        "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "]", "^", "_",
        "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n",
        "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|",
        "}", "~",
    )
    password_list = random.choices(symbols, k=length)
    password = "".join(password_list)
    return password


class SignupAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        try:
            instance = User.objects.get(
                username=request.data["username"], email=request.data["email"]
            )
        except:
            instance = None
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            password = create_password()
            user.set_password(password)
            user.save()
            send_mail(
                "Your confirmation code",
                f"{password}",
                "from@example.com",
                (user.email,),
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersList(ListModelMixin, CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserManagementSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination5
    search_fields = ("username",)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def final_create(self, password, user, serializer):
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    lookup_field = "username"

    def get_serializer_class(self):
        if self.request.method == "DELETE":
            return DestroyUserSerializer
        return AdminUserManagementSerializer


class MeViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ChangingUserDataSerializer
        return AdminUserManagementSerializer

    def retrieve(self, request):
        queryset = User.objects.all()
        me = get_object_or_404(queryset, pk=self.request.user.id)
        serializer = self.get_serializer_class()
        serializer = serializer(me)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        me = get_object_or_404(User, pk=self.request.user.id)
        serializer = self.get_serializer_class()
        serializer = serializer(me, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer
