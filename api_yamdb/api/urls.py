from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
#    Ресурс auth: аутентификация.
#    Ресурс users: пользователи.
#    Ресурс titles: произведения, к которым пишут отзывы (определённый фильм,
#       книга или песенка).
#    Ресурс categories: категории (типы) произведений
#       («Фильмы», «Книги», «Музыка»).
#    Ресурс genres: жанры произведений. Одно произведение может быть привязано
#       к нескольким жанрам.
#    Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому
#       произведению.
#    Ресурс comments: комментарии к отзывам. Комментарий привязан к
#       определённому отзыву.
