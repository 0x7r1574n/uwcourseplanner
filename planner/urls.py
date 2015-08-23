from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.course_list, name='course_list'),
    url(r'^planner/(?P<pk>[0-9]+)/$', views.course_detail, name='course_detail'),
    url(r'^planner/new/$', views.course_new, name='course_new'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'courseapi/$', views.rest_course_list, name='course-list'),
    url(r'courseapi/(?P<pk>[0-9]+)/$', views.rest_course_detail, name='core-course-detail'),
    url(r'coreapi/$', views.RestCoreList.as_view(), name='core-course-list'),
]
