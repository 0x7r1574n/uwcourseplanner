from django.db import models


class Course(models.Model):
    fullname = models.CharField(max_length=10)
    dept = models.CharField(max_length=10)
    number = models.IntegerField()
    title = models.CharField(max_length=50)
