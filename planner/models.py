from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    user = models.ForeignKey('auth.User')
    dept = models.CharField(max_length=50)
    number = models.IntegerField()
    fullname = dept.lower().replace(' ', '') + str(number)
    credit = models.IntegerField()
    year = models.IntegerField()
    quarter = models.IntegerField()
    title = models.CharField(max_length=150)
