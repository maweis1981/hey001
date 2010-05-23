from django.db import models
from published_manager import settings

class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(state=settings.STATE_PUBLISHED)
