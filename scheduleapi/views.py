import django_filters
from .models import Course
from .serializers import CourseSerializer
from rest_framework import generics


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = ['fullname', 'dept', 'number', 'title']
