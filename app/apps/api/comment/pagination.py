from rest_framework.pagination import PageNumberPagination


class CommentdResultsSetPagination(PageNumberPagination):
    page_size = 5