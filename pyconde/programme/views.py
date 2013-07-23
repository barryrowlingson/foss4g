
from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from pyconde.booking import models as booking_models
from pyconde.conference import models as conference_models

from models import Presentation,PSession,Person

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

@staff_member_required
def view_people(request):
    peeps = Person.objects.all()
    context = {'people': peeps}
    return render_to_response("programme/view_people.html",
                              context,
                              context_instance=RequestContext(request))


@staff_member_required
def view_person(request,person_pk):
    try:
        person = Person.objects.select_related(depth=2).get(pk=person_pk)
    except:
        raise Http404
    context = {'person': person}
    return render_to_response("programme/view_person.html",
                              context,
                              context_instance=RequestContext(request))
 
    pass

from utils import useless
@staff_member_required
def rolecounts(request):
    p = useless()
    context = {"people": p}
    return render_to_response("programme/rolecounts.html",
                               context,
                               context_instance=RequestContext(request))
   

@staff_member_required
def timetable1(request):
    sessions = PSession.objects.all().order_by("start").prefetch_related("presentation_set")#.order_by("location")
    context = {"sessions": sessions}
    return render_to_response("programme/time1.html",
                              context,
                              context_instance=RequestContext(request)
                              )


@staff_member_required
def nameindex(request):
    people = Person.objects.all().prefetch_related("presentation_set","presenter")
    for p in people:
        splitname = p.name.split()
        p.lastname = splitname[-1]
        p.firstname = " ".join(splitname[:-1])
        p.pres=[]
        p.copres=[]
        for pres in p.presenter.all():
            if pres.insession:
                p.pres.append(pres.insession.title)
        for pres in p.presentation_set.all():
            if pres.insession:
                p.copres.append(pres.insession.title)
        p.pres = sorted(list(set(p.pres)))
        p.copres = sorted(list(set(p.copres)))
        p.sum=len(p.pres)+len(p.copres)

    people=sorted(people,key=lambda x: x.lastname)
    people = filter(lambda x: x.sum>0, people)
    return render_to_response("programme/nameindex.html",
                              {"people":people},
                              context_instance=RequestContext(request)
                              )


def lastname(p):
    return p.name.split()[-1]

def lastnamesort(ps):
    return sorted(ps,key=lastname)

def proofing(request):
    P = Presentation.objects.filter(insession__gt=0).order_by("insession").prefetch_related("presenter","copresenter") #.values("title","copresenter__name","presenter__name","id","abstract")
    Phash = dict((p.id, p) for p in P)
    S = PSession.objects.all().order_by("start").prefetch_related("location","presentation_set")
    context = {"Phash": Phash,
               "S": S}
    return render_to_response("programme/proofing.html",
                              context,
                              context_instance=RequestContext(request)
                              )

