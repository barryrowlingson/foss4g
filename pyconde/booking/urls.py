from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.contrib.auth import forms
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.book, name='booking-index'),
#    url(r'^$', views.book, name='booking-book'),
                       url(r'^summary$', views.summary, name='booking-summary'),
                       url(r'^bookreport$', views.bookreport, name='booking-bookreport'),
                       url(r'^adminreport$', views.secretbookreport,name='booking-secretbookreport'),
                       url(r'^spendreport$', views.secretspending,name='spending-secretbookreport'),
                       url(r'^refundreport$', views.refundreport,name='booking-refundreport'),
                       url(r'^logout$', views.logout_user, name='booking-logout'),
                       url(r'^login$', views.login_user, name='booking-login'),
                       url(r'^adduser$', views.add_workshopper, name='booking-adduser'),
                       url(r'^regdesk$', views.registrationreport, name='booking-regreport'),
                       
    )

