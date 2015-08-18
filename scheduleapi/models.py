from django.db import models


class Course(models.Model):
    fullname = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    number = models.IntegerField()
    title = models.CharField(max_length=150)
    description = models.URLField()

    class Meta:
        ordering = ('dept', 'number')
