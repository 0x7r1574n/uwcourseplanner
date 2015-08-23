from rest_framework import serializers
from .models import Course, Core


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('user', 'fullname', 'dept', 'number', 'credit', 'year', 'quarter', 'title', 'description')


class CoreSerializer(serializers.ModelSerializer):
    prereq = serializers.CharField(max_length=50, allow_blank=True, required=False)

    class Meta:
        model = Core
        fields = ('fullname', 'prereq')
