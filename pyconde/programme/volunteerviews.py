from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from models import Presentation,PSession,Person,PlenarySession,CWorkshop, SpecialEvent, Volunteering

from django.contrib.admin.views.decorators import staff_member_required

import datetime
import locale

from collections import defaultdict

@staff_member_required
def forevent(request,vid):
    vevent = get_object_or_404(Volunteering, pk=vid)
    context = {'vevent': vevent}
    return render_to_response("programme/vevent.html",
                              context,
                              context_instance=RequestContext(request))
 

@staff_member_required
def forperson(request,pid):
    person = get_object_or_404(Person, pk=pid)
    # get person's chairing, session helping, workshop helping, volunteering

    raise Http404,"not written yet"

@staff_member_required
def events(request):
    vevents = Volunteering.objects.all().order_by("start")
    context = {'vevents': vevents}
    return render_to_response("programme/vevents.html",
                              context,
                              context_instance=RequestContext(request))
@staff_member_required
def forday(request,daynumber):
    try:
        daynumber=int(daynumber)
    except:
        raise Http404,"Day number not found"
    if daynumber < 1 or daynumber > settings.NUM_DAYS:
        raise Http404,"Day not found"
    day = settings.ALL_DAYS[daynumber-1]

    sessions = PSession.objects.filter(start__contains=day).select_related("location","chair","helper").order_by("start")
    context = {'sessions': sessions, 'day': day}
    return render_to_response("programme/vsessions.html",
                              context,
                              context_instance=RequestContext(request))
@staff_member_required
def workshops(request):
    cws = CWorkshop.objects.all().select_related("presenter","helper","location").order_by("start")
    context = {'cws': cws}
    return render_to_response("programme/vworkshops.html",
                              context,
                              context_instance=RequestContext(request))

def seshdata(s,doing):
    return {'start': s.start,
            'location': s.location,
            'title': doing}

def cwsdata(cws):
    return seshdata(cws,"Helping %s" % cws.title)

def evdata(ev):
    ev.location=""
    return seshdata(ev,ev.title) 

@staff_member_required
def volunteers(request):
    vdata = volunteerdata()
    context = {'vdata': vdata}
    return render_to_response("programme/vroster.html",
                              context,
                              context_instance=RequestContext(request))


def volunteerdata():
# 
# get all the things people can volunteer for
#
    sessions = PSession.objects.all().select_related("location","chair","helper").order_by("start")
    cws = CWorkshop.objects.all().select_related("presenter","helper","location").order_by("start")
    vevents = Volunteering.objects.all().order_by("start")
    
    vs = defaultdict(list)
    for s in sessions:
        vs[s.helper].append(seshdata(s,"Helping %s" % s.title))
        vs[s.chair].append(seshdata(s,"Chairing %s" % s.title))
        
    for c in cws:
        vs[c.helper].append(cwsdata(c))

    for v in vevents:
        for vol in v.volunteer.all():
            vs[vol].append(evdata(v))
        
    del vs[None]

    # sort the activities by start
    vs = dict(vs)
    [v.sort(key=lambda k:k['start']) for v in vs.values()]
    
    # sort the records by person's name
    vs = [(k,v) for k,v in vs.iteritems()]
    vs.sort(key=lambda x:x[0].name)
    return vs
    
@staff_member_required
def index(request):
    return render_to_response("programme/volindex.html",
                              {},
                              context_instance=RequestContext(request))
