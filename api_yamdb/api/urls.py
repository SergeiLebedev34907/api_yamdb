from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "api"

router = routers.DefaultRouter()

# Вторая часть
router.register("titles", views.TitlesViewSet, basename='title')
router.register("genres", views.GenreViewSet, basename='genre')
router.register("categories", views.CategoryViewSet, basename='category')
# Конец второй части
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    views.ReviewViewSet,
    basename="reviews",
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    views.CommentViewSet,
    basename="comments",
)

urlpatterns = [
    # 3 часть
    path("v1/", include(router.urls)),
    # 1 часть
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
