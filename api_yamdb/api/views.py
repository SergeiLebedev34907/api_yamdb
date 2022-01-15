from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Title, Comment
from .pagination import ReviewAndCommentPagination
from .permissions import IsAuthorModeratorAdminOrReadOnly
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = ReviewAndCommentPagination
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        new_queryset = Review.objects.filter(title=title)

        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, title=get_object_or_404(
            Title, id=self.kwargs.get('title_id')))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = ReviewAndCommentPagination
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        new_queryset = Comment.objects.filter(review=review)

        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, review=get_object_or_404(
            Review, id=self.kwargs.get('review_id')))
