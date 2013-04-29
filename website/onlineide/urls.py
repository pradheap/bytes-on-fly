from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from onlineide.views import *

urlpatterns = patterns('onlineide.views', 
    url(r'^$', 'index'),
    url(r'^snippets/$', SnippetCreate.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', SnippetDetail.as_view()),
    url(r'^output/(?P<pk>\d+)/$', FilestatsDetail.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)

urlpatterns = format_suffix_patterns(urlpatterns)
