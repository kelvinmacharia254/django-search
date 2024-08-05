# replace 'yourapp' with the name of your app
# change model name add necessary fields to the search vector

from django.core.management.base import BaseCommand

from django.contrib.postgres.search import SearchVector
from quotes.models import Quote

class Command(BaseCommand):
    help = "Update search vector field in the database for existing an dataset"

    def handle(self, *args, **options):
        print("... updating search_vector field. Be patient ...")
        quotes = Quote.objects.all()
        for quote in quotes:
            quote.search_vector = (
                SearchVector('name') + SearchVector('quote')
            )
            quote.save()

        print("Completed!!! Search vector updated successfully.")