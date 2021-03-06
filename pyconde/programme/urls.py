from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.contrib.auth import forms
from django.contrib.auth import views as auth_views

from . import views
from . import volunteerviews

# / - main timetable
# /workshops - workshop timetable with booking info
# /workshops/{id} - workshop info
# /presentation/{id} presentation info

# TODO URL for session

urlpatterns = patterns('',
                       url(r'^$', views.index, name='programme-index'), # was default index page

                       url(r'^index2$',views.timetable1,name='old-index'), # new index page
                       url(r'^proof$',views.proofing,name='proofing'),

                       url(r'^workshops$', views.workshops, name='workshop-index'),
                       url(r'^workshops/(?P<workshop_pk>\d+)/$', views.view_workshop, name='view-workshop'),

                       url(r'^freeworkshops$', views.freeworkshops, name="freeworkshop-index"),
                       url(r'^freeworkshops/(?P<pk>\d+)/$', views.freeworkshop, name="freeworkshop"),
                       url(r'^freeworkshoplist$', views.freeworkshoplist,name="freeworkshoplist"),

                       url(r'^plenary/(?P<pk>\d+)/$', views.view_plenary, name='view-plenary'),
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

                       url(r'^presenterdetails/$', views.presenterdetails,name='presenter-details'),

                       url(r'^daily/(?P<daynumber>\d+)/$',views.timetabletest,name='view-timetable'),

                       url(r'^tags/(?P<slug>[-\w]+)/$', views.taggedpresentations, name='tagged-pres'),

                       url(r'^favourites/$', views.favourites,name='favourites'),
                       url(r'^favourites/calendar$', views.favouritescalendar,name='favouritescalendar'),
                       url(r'^favourite/(?P<presentation_pk>\d+)/', views.favourite, name='favourite'),
                       url(r'^unfave/(?P<presentation_pk>\d+)/', views.unfave, name='unfave'),
                       url(r'^togglefave/(?P<presentation_pk>\d+)/', views.togglefave, name='togglefave'),
                       url(r'^preslist/', views.preslist, name='preslist'),
                       url(r'^wspreslist/', views.wspreslist, name='wspreslist'),

                       url(r'^search/', include('haystack.urls')),

                       url(r'volunteer/events/',volunteerviews.events,name="volunteerevents"),
                       url(r'volunteer/event/(?P<vid>\d+)/',volunteerviews.forevent,name="volunteerevent"),
                       url(r'volunteer/person/(?P<pid>\d+)/',volunteerviews.forperson,name="volunteerperson"),
                       url(r'volunteer/sessions/(?P<daynumber>\d+)/',volunteerviews.forday,name="volunteersessions"),
                       url(r'volunteer/workshops/',volunteerviews.workshops,name="volunteerworkshops"),
                       url(r'volunteer/roster/',volunteerviews.volunteers,name="volunteerroster"),
                       url(r'volunteer/',volunteerviews.index,name="volunteerindex"),

                       
                       
                       )

