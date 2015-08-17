from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns 
from scheduleapi import views

urlpatterns = [
    url(r'api/$', views.CourseList.as_view(), name='course-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
