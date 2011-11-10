from django.db import models


class Address(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=5)
    city = models.ForeignKey('City')

    class Meta:
        db_table = u'address'
        managed = False

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class City(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = u'city'
        managed = False

    def __unicode__(self):
        return self.name
