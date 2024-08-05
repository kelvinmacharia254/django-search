from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank, SearchHeadline
from django.db.models import F # F is used to reference a field in queries

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
        Implement basic textual search

        Implement fulltext search with postgres support in Django

        """
        # Get the search query from the GET parameters
        query = self.request.GET.get("q")
        if query:
            # Create a search query object from the user's input
            search_query = SearchQuery(query)
            # Reference the search_vector field in the model
            search_vector = F('search_vector')
            # Calculate the rank of each record based on how well it matches the search query
            search_rank = SearchRank(F('search_vector'), search_query)
            # Create a highlighted snippet of the matched text within the quote field
            search_headline = SearchHeadline("quote", search_query)
            # Annotate the queryset with the search vector, rank, and headline
            queryset = Quote.objects.annotate(search=search_vector, rank=search_rank).annotate(headline=search_headline).filter(search_vector=search_query).order_by('-rank')
        else:
            # Return an empty queryset if no search term is provided
            queryset = Quote.objects.none()

        return queryset

'''
Detailed Comments:
query = self.request.GET.get("q"):

Retrieves the search query parameter from the GET request. If the parameter q is present in the request URL, its value will be assigned to query.
if query::

Checks if the query variable is not empty. This ensures that the search operation only proceeds if there is a search term provided by the user.
search_query = SearchQuery(query):

Converts the user's search input into a SearchQuery object. This object is used for performing full-text searches in PostgreSQL.
search_vector = F('search_vector'):

Uses Django’s F expression to reference the search_vector field of the Quote model. This field contains the precomputed search vectors for the quotes.
search_rank = SearchRank(search_vector, search_query):

Computes a rank for each record in the queryset based on how well the search_vector matches the search_query. Higher ranks indicate better matches.
search_headline = SearchHeadline("quote", search_query):

Generates a highlighted version of the quote field where the search terms are emphasized. This is useful for displaying search results with context around the matched terms.
queryset = Quote.objects.annotate(search=search_vector, rank=search_rank).annotate(headline=search_headline).filter(search_vector=search_query).order_by('-rank'):

Annotates the queryset with the search_vector, rank, and headline fields.
Filters the queryset to include only those records whose search_vector matches the search_query.
Orders the results by rank in descending order, so the most relevant results appear first.
else: queryset = Quote.objects.none():

If no search query is provided, returns an empty queryset. This avoids returning all quotes when no search term is specified.
return queryset:

Returns the final queryset, which is either the filtered and annotated search results or an empty queryset if no search term was provided.
This implementation ensures that your search results are relevant and well-ranked, with highlights around the matched terms in the quotes.
'''

