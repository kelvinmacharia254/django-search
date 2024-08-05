from django.db import models

# Boost postgres Full-text-search performance by
#   1. Save the search vector with a SearchVectorField rather can converting during search(on the fly)
#   2. Create a database index to speed up data retrieval process on the db.
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Quote(models.Model):
    name = models.CharField(max_length=250)
    quote = models.TextField(max_length=1000)
    search_vector = SearchVectorField(null=True) # can be updated automatically via post save signal

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

    def __str__(self):
        return self.quote
