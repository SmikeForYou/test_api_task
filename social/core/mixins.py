from django.db import models


class DateAddedMixin(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True