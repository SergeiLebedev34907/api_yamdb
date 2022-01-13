from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("v1/auth/signup/", views.SignupAPIView.as_view(), name="signup"),
    path(
        "v1/auth/token/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("v1/users/", views.UsersList.as_view()),
    path(
        "v1/users/me/",
        views.MeViewSet.as_view({"get": "retrieve", "patch": "update"}),
    ),
    path("v1/users/<str:username>/", views.UsersDetail.as_view()),
]
