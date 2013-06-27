
from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from pyconde.booking import models as booking_models
from pyconde.conference import models as conference_models

from models import Presentation,PSession

from django.contrib.admin.views.decorators import staff_member_required

import datetime

def index(request):
    context = {}
    return render_to_response("programme/index.html",
                              context,
                              context_instance=RequestContext(request))

def workshops(request):
    ws = booking_models.Workshop.objects.select_related(depth=4).order_by("item__start")
    for w in ws:
        w.busycode = w.busy()
        w.wcode = w.item.title.split(":")[0]

    context = {
        "workshops":ws
        }
    return render_to_response("programme/workshops.html",
                              context,
                              context_instance=RequestContext(request))


def view_workshop(request, workshop_pk):
    #w = get_object_or_404(booking_models.Workshop,pk=workshop_pk)
    try:
        w = booking_models.Workshop.objects.select_related(depth=4).get(pk=workshop_pk)
    except:
        raise Http404
    w.busycode = w.busy()
    context = {"w":w}
    return render_to_response("programme/view_workshop.html",
                              context,
                              context_instance=RequestContext(request))
@staff_member_required
def view_presentation(request, presentation_pk):
    try:
        pres = Presentation.objects.select_related(depth=2).get(pk = presentation_pk)
    except:
        raise Http404
    sesh = pres.insession
    if sesh:
        pres.start = sesh.start + (pres.position-1)*datetime.timedelta(minutes=sesh.talkduration)
    else:
        pres.start = "unscheduled"
    context = {'pres': pres}
    return render_to_response("programme/view_presentation.html",
                              context,
                              context_instance=RequestContext(request))
@staff_member_required
def view_psessions(request):
    seshes = PSession.objects.select_related(depth=4).all().order_by("start")
    context = {'seshes': seshes}
    return render_to_response("programme/view_psessions.html",
                              context,
                              context_instance=RequestContext(request))
    
@staff_member_required
def view_presentations(request):
    presses = Presentation.objects.select_related(depth=3).all()
    context = {"presentations": presses}
    return render_to_response("programme/view_presentations.html",
                              context,
                              context_instance=RequestContext(request))
   
@staff_member_required
def view_psession(request, psession_pk):
    try:
        psesh = PSession.objects.select_related(depth=2).get(pk = psession_pk)
    except:
        raise Http404
    presses = psesh.presentation_set.all().select_related(depth=2).order_by("position")
    context = {'psesh': psesh,
               'presses': presses}
    return render_to_response("programme/view_psession.html",
                              context,
                              context_instance=RequestContext(request))

@staff_member_required
def view_location(request,location_slug):
    loc = get_object_or_404(conference_models.Location,slug=location_slug)
    context={"loc":loc}
    return render_to_response("programme/view_location.html",
                               context,
                               context_instance=RequestContext(request))