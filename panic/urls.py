from django.conf.urls import patterns, url
from panic import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'test', views.test, name='test'),
                       url(r'inform', views.inform, name='inform'),
                       url(r'random/([0-9])', views.random, name='random'),
                       url(r'(?P<pk>[0-9]+)', views.DetailView.as_view()),
                       url(r'(?P<name>\w+)', views.contact, name='contact'),
                       )
