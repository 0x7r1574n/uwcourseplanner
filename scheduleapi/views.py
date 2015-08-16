from .models import Course
from .serializers import CourseSerializer
from rest_framework import generics


class CourseCreate(generics.CreateAPIView):
    serializer_class = CourseSerializer
    model = Course


class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer