
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

def gallery(request):
    maps = Map.objects.all().order_by("?")
    context={'maps': maps}
    return render_to_response("mapgallery/index.html",
                              context,
                              context_instance=RequestContext(request))
            

@staff_member_required
def results(request):
    maps = list(Map.objects.all())
    maps.sort(key = lambda x:-x.vote_total)
    context={'maps': maps}
    return render_to_response("mapgallery/results.html",
                              context,
                              context_instance=RequestContext(request))

