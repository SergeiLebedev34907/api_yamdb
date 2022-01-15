from rest_framework.pagination import PageNumberPagination


class ReviewAndCommentPagination(PageNumberPagination):
    page_size = 5
