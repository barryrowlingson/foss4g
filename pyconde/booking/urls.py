from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='booking-index'),
    url(r'^book$', views.book, name='booking-book'),
    url(r'^logout$', views.logout_user, name='booking-logout'),
    url(r'^login$', views.login_user, name='booking-login'),
    )

