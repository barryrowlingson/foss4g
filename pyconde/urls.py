# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^accounts/profile', 'django.views.defaults.page_not_found'),
    url(r'^accounts/register', 'django.views.defaults.page_not_found'),
#    url(r'^tickets/', include('pyconde.attendees.urls')),
    url(r'^accounts/', include('pyconde.accounts.urls')),
    url(r'^accounts/', include('userprofiles.urls')),
#    url(r'^reviews/', include('pyconde.reviews.urls')),
#    url(r'^schedule/', include('pyconde.schedule.urls')),
#    url(r'^proposals/', include('pyconde.proposals.urls')),
#    url(r'^helpdesk/', include('helpdesk.urls')),
#    url(r'^search/', include('pyconde.search.urls')),
    url(r'^booking/', include('pyconde.booking.urls')),
#    url(r'^', include('cms.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
