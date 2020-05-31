from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PaginationView(object):
    def paginate(request, objects_list, num_pages=5):
        paginator = Paginator(objects_list, num_pages)
        page = request.GET.get('page')
        try:
            objects_page = paginator.page(page)
        except PageNotAnInteger:
            objects_page = paginator.page(1)
        except EmptyPage:
            objects_page = paginator.page(paginator.num_pages)

        return objects_page, paginator
