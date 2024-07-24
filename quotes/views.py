from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from .models import Quote


@method_decorator(cache_page(60 * 5), name="dispatch")
class QuoteList(ListView):
    model = Quote
    context_object_name = "quotes"
    template_name = "quote.html"


class SearchResultsList(ListView):
    model = Quote
    context_object_name = "quotes"
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        print(query)
        return Quote.objects.filter(Q(name__icontains=query)|Q(quote__icontains=query))


