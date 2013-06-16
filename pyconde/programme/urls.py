from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.contrib.auth import forms
from django.contrib.auth import views as auth_views

from . import views

# / - main timetable
# /workshops - workshop timetable with booking info
# /workshops/{id} - workshop info
# /presentation/{id} presentation info

urlpatterns = patterns('',
                       url(r'^$', views.index, name='programme-index'), 
                       url(r'^workshops$', views.workshops, name='workshop-index'),
                       url(r'^workshops/(?P<workshop_pk>\d+)/$', views.view_workshop, name='view-workshop'),
                       url(r'^presentations/(?P<presentation_pk>\d+)/$', views.view_presentation, name='view-presentation'),
                       url(r'^locations/(?P<location_slug>[-\w]+)/$', views.view_location, name='view-location'),
                       )

