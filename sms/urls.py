from django.conf.urls import patterns, url
from sms import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'template/(?P<pk>[0-9]+)', views.TemplateView.as_view()),
                       )
