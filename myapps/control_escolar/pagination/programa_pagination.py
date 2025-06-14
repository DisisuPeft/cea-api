from rest_framework.pagination import PageNumberPagination

class ProgramaPagination(PageNumberPagination):
    page_size = 10