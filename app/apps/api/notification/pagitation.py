from rest_framework.pagination import PageNumberPagination


class NotificationPaginator(PageNumberPagination):
	page_size = 10