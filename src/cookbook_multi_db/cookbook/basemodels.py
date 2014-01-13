from django.db import models
from django.utils.timezone import now


class DateTimeInfo(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(DateTimeInfo, self).save(*args, **kwargs)
