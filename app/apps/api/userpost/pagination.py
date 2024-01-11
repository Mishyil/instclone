from rest_framework.pagination import PageNumberPagination


class ProfilePostPagination(PageNumberPagination):
	page_size = 9