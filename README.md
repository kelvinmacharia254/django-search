## Search feature in Django

This project explores the possible techniques we can use to search data in our Django application.

### 1. Basic search in Django

### 2. Searching using postgres fulltext search support in Django


Reference: 

[Basic and Full-text Search with Django and Postgres by](https://testdriven.io/blog/django-search/#:~:text=of%20the%20code.-,Basic%20Search,OR%20(%20%7C%20)%20logical%20operators.&text=Here%2C%20we%20used%20the%20filter,the%20name%20or%20quote%20fields.) 
[Samuel Torimiro](https://testdriven.io/authors/torimiro/)

```
class SearchResultsList(ListView):
    model = Quote
    context_object_name = "quotes"
    template_name = "search.html"

    def get_queryset(self):
        """
        Implement basic textual search

        Implement fulltext search with postgres support in Django

        The implementation have been numbered using comments, comment in and out to test each as numbered
        """
        query = self.request.GET.get("q")
        if query:
            # 1. Basic search
            # queryset = Quote.objects.filter(Q(name__icontains=query)|Q(quote__icontains=query))

            # 2. Fulltext search using postgres support in django
            #     2(a). Single Field Search
            #       search by a single field 'quote'
            # queryset = Quote.objects.filter(quote__search=query)

            #     2(b). Multiple Field Search
            # search_query = SearchQuery(query) # get query from request object
            # search_vector = SearchVector('name', 'quote')
            # queryset = Quote.objects.annotate(search=search_vector).filter(search=search_query)

            #     2(c). Multiple Field Search with stemming and ranking
            #           Stemming: Process of reducing words to their stem base or root form such that tenses and plurals will be treated as similar words.
            #               e.g. child and children are treated as same in the search.
            #           Ranking allows us ordering results by relevance
            #           Searching with the two allows more powerful, precise and relevant search
            # search_query = SearchQuery(query) # get query from request object
            # search_vector = SearchVector('name', 'quote')
            # search_rank=SearchRank(search_vector, search_query)
            # queryset = Quote.objects.annotate(search=search_vector, rank=search_rank).filter(search=search_query).order_by('-rank')

            #     2(d). Multiple Field Search with weights
            #           With FTS you can add more importance to some fields over others to refine search.
            #           Weights take letters A,B,C,D which refers to numbers 1.0, 0.4, 0.2 and 0.1 respectively.
            search_query = SearchQuery(query) # get query from request object
            #           assign weights to fields in the vector, quote field will prevail over name field because of the higher weight
            search_vector = SearchVector('name', weight='B') + SearchVector('quote', weight='A')
            search_rank=SearchRank(search_vector, search_query)  #
            #           We can also add a SearchHeadline:- allows a little preview of the search results
            search_headline = SearchHeadline('quote', search_query) # takes field you want to preview along with the query
            # filter results to display ones with rank>0.3
            queryset = Quote.objects.annotate(search=search_vector, rank=search_rank).annotate(headline=search_headline).filter(rank__gte=0.3).order_by('-rank')

        else:
            # Return an empty queryset if no search term is provided
            queryset = Quote.objects.none()

        return queryset
```