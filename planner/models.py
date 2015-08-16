from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    user = models.ForeignKey('auth.User')
    fullname = models.CharField(max_length=10)
    dept = models.CharField(max_length=10)
    number = models.IntegerField()
    credit = models.IntegerField()
    year = models.IntegerField()
    quarter = models.IntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField()
