import random

from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from api.filters import TitleFilter
from reviews.models import Category, Comment, Genre, Review, Title
from .pagination import PageNumberPagination5
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorModeratorAdminOrReadOnly
from .serializers import (
    AdminUserManagementSerializer,
    CategorySerializer,
    ChangingUserDataSerializer,
    CommentSerializer,
    CustomTokenObtainPairSerializer,
    DestroyUserSerializer,
    GenreSerializer,
    TitleCreateSerializer,
    TitleListSerializer,
    ReviewSerializer,
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


# 3 часть
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination5
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        new_queryset = Review.objects.filter(title=title)

        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            title=get_object_or_404(Title, id=self.kwargs.get("title_id")),
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination5
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = Comment.objects.filter(review=review)

        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get("review_id")),
        )


# Вторая часть
class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               viewsets.GenericViewSet):

    pass


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by('id')
    pagination_class = PageNumberPagination5
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TitleFilter
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination5
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination5
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
# Конец второй части
