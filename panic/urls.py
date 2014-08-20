from django.conf.urls import patterns, url
from panic import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'(?P<pk>[0-9]+)', views.DetailView.as_view()),
                       )
