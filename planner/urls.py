from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.course_list, name='course_list'),
    url(r'^planner/(?P<pk>[0-9]+)/$', views.course_detail, name='course_detail'),
    url(r'^planner/new/$', views.course_new, name='course_new'),
    url(r'^planner/(?P<pk>[0-9]+)/edit/$', views.course_edit, name='course_edit'),
    url(r'^/accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^/accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/urlexpand'}),
]
