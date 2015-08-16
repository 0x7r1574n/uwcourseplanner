from django.db import models
import requests
import bs4


class Course(models.Model):
    fullName = models.CharField(max_length=10)
    dept = models.CharField(max_length=10)
    number = models.IntegerField()
    credit = models.IntegerField()
    title = models.CharField(max_length=50)
