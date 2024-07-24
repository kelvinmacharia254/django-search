from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from django.contrib.postgres.search import SearchVector,SearchQuery

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
        """
        Implement basic search with Django ORM lookups

        Implement fulltext search with postgres support in Django

        The implementation have been numbered using comments, comment in and out to test each as numbered
        """
        query = self.request.GET.get("q")
        if query:
            # 1. Basic search feature with ORM lookups
            # queryset = Quote.objects.filter(Q(name__icontains=query)|Q(quote__icontains=query))

            # 2. Basic implementation of Fulltext search using postgres
            #   Create the search vector and search query
            search_vector = SearchVector('name', 'quote') # search db using this fields. Create a searchable vector
            search_query = query # query from request object
            #   Annotate and filter the queryset
            queryset = Quote.objects.annotate(search=search_vector).filter(search=search_query)

            # 2. Implementation of Fulltext search with Stemming and Ranking using postgres
            #   Create the search vector and search query

            # search_vector = SearchVector('name', 'quote') # search db using this fields
            # search_query = SearchQuery(query) # query from request object

            #   Annotate and filter the queryset
            # queryset = Quote.objects.annotate(search=search_vector).filter(search=search_query)

            # 3.


        else:
            # Return an empty queryset if no search term is provided
            queryset = Quote.objects.none()


        return queryset


