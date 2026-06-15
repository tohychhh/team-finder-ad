from django.core.paginator import Paginator
from team_finder.constants import PAGINATION_PAGE_SIZE


def paginate_queryset(queryset, request):
    paginator = Paginator(queryset, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)