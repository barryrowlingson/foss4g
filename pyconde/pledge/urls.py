from django.conf.urls import patterns, url
from django.conf import settings

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.pledgelist, name='pledge-list'),
    )

