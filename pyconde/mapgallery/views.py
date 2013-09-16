
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from django.contrib.admin.views.decorators import staff_member_required

from .models import Map

LOCAL="http://localhost:8080/mapgallery/"
REMOTE="http://www.rowlingson.com/FOSS4G/mapgallery/"
ARCHIVE=REMOTE

def gallery(request):
    maps = Map.objects.all().order_by("?")
    context={'maps': maps,
             'classes': ['c1','c2'],
             'archive':ARCHIVE}
    return render_to_response("mapgallery/index.html",
                              context,
                              context_instance=RequestContext(request))
            

@staff_member_required
def results(request):
    maps = list(Map.objects.all())
    maps.sort(key = lambda x:-x.vote_total)
    context={'maps': maps,'archive':ARCHIVE}
    return render_to_response("mapgallery/results.html",
                              context,
                              context_instance=RequestContext(request))

def getlink(map):
    if map.format == "PDF":
        return ARCHIVE+map.directory+"/"+map.directory+".pdf"
    if map.format == "URL":
        return map.URL
    if map.format == "Movie":
        return map.URL
    if map.format == "PNG":
        return ARCHIVE+map.directory+"/"+map.directory+".png"
    return None

def mapmodal(request,idcode):
    map = get_object_or_404(Map,id=idcode)
    map.linkto = getlink(map)
    context={'map':map,
             'archive':ARCHIVE}
    return render_to_response("mapgallery/boxcontent.html",
                              context,
                              context_instance=RequestContext(request))
    
