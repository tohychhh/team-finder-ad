from django.core.paginator import Paginator

from team_finder.constants import PAGINATION_PAGE_SIZE


def paginate_queryset(queryset, request, page_size=PAGINATION_PAGE_SIZE):
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
