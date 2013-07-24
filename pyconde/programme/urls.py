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

# TODO URL for session

urlpatterns = patterns('',
                       url(r'^$', views.index, name='programme-index'), 

                       url(r'^time1$',views.timetable1,name='timetable1'),
                       url(r'^proof$',views.proofing,name='proofing'),

                       url(r'^workshops$', views.workshops, name='workshop-index'),
                       url(r'^workshops/(?P<workshop_pk>\d+)/$', views.view_workshop, name='view-workshop'),

                       url(r'^presentations/(?P<presentation_pk>\d+)/$', views.view_presentation, name='view-presentation'),
                       url(r'^presentations/$', views.view_presentations, name='view-presentations'),

                       url(r'^sessions/$', views.view_psessions, name='view-psessions'),
                       url(r'^sessions/(?P<psession_pk>\d+)/$', views.view_psession, name='view-psession'),

                       url(r'^people/$', views.view_people, name='view-people'),
                       url(r'^people/(?P<person_pk>\d+)/$', views.view_person, name='view-person'),

                       url(r'^locations/(?P<location_slug>[-\w]+)/$', views.view_location, name='view-location'),

                       url(r'^admin/rolecounts/$',views.rolecounts,name='view-rolecount'),

                       url(r'^designer/nameindex/$',views.nameindex,name='view-nameindex'),
                       url(r'^designer/timetable/$',views.destimetable,name='view-destimetable'),
                       url(r'^designer/fulllisting/$',views.fulllisting,name='view-fullisting'),


                       )

