from rest_framework.pagination import PageNumberPagination

class CicloPagination(PageNumberPagination):
    page_size = 10
    
    
class PeriodosPagination(PageNumberPagination):
    page_size = 10