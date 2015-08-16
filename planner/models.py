from django.db import models
from django.contrib.auth.models import User



class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Course(models.Model):
    user = models.ForeignKey('auth.User')
    fullname = models.CharField(max_length=10)
    dept = models.CharField(max_length=10)
    number = models.IntegerField()
    credit = models.IntegerField()
    year = models.IntegerField()
    quarter = fields.IntegerRangeField(min_value=1, max_value=4)
    title = models.CharField(max_length=50)
    description = models.TextField()
