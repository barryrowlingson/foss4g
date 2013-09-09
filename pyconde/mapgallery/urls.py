from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.gallery, name='gallery'), 
                       url(r'^results$', views.results, name='gallery'), 
                       )


  
