from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns 
from scheduleapi import views

urlpatterns = [
    url(r'post/$', views.CourseCreate.as_view(), name='course-create'),
    url(r'^courses/(?P<pk>[0-9]+)/$', views.CourseDetail.as_view(), name='course-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
