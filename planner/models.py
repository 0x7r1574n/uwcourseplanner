from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    user = models.ForeignKey('auth.User')
    fullname = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    number = models.IntegerField()
    credit = models.IntegerField()
    year = models.IntegerField()
    quarter = models.IntegerField()
    title = models.CharField(max_length=150)

    class Meta:
        ordering = ('year', 'quarter', 'dept', 'number')
