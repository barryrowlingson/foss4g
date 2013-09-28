from django.conf.urls import patterns, url
from django.conf import settings

from . import views

# toggle the commented lines here for when you are collecting pledges.
urlpatterns = patterns('',
#                       url(r'^$', views.pledgelist, name='pledge-list'),
                       url(r'^$', views.pledgeall, name='pledge-all'),
#                       url(r'^create$', views.pledgecreate, name='pledge-create'),
    )

