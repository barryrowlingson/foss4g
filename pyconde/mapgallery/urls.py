from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.gallery, name='gallery'), 
                       url(r'^results$', views.results, name='results'), 
                       url(r'^winners$', views.winners, name='winners'), 
                       url(r'^boxcontent/(?P<idcode>\d+)/$', views.mapmodal, name='mapmodal'), 
                       )


  
