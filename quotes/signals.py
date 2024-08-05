from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector

# update the search vector field for each new record
@receiver(post_save, sender=Quote)
def update_search_vector(sender, instance, **kwargs):
    instance.search_vector = (
        SearchVector('name') + SearchVector('quote')
    )
    instance.save()
