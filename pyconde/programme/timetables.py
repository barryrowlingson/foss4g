from models import Presentation,PSession,Person,PlenarySession,CWorkshop,GlobalEvent,SpecialEvent

from timetabling import TimeTable
from collections import defaultdict
import taggit

import datetime

def daterange(start_datetime, end_datetime, delta):
    current = start_datetime
    while current < end_datetime:
        yield current
        current = current + delta

def time1(day, grain=30, faves=[]):
    #presentations = Presentation.objects.all()

    #1 add the global events
    #2 add the plenaries
    #3 add the sessions

    sessions = PSession.objects.filter(start__contains=day).select_related("location","chair","helper")
    presses = Presentation.objects.filter(insession__in=sessions).select_related("insession","presenter")

    Phash = defaultdict(list)
    for p in presses:
        Phash[p.insession].append(p)

    alltags = taggit.models.TaggedItem.objects.filter(presentation__in=presses).select_related("tag","content_object")
    Taghash = defaultdict(list)
    for t in alltags:
        Taghash[t.object_id].append(t.tag)

    globalevents = GlobalEvent.objects.filter(start__contains=day)
    plenaries = PlenarySession.objects.filter(start__contains=day)
    #sessions = filter(lambda x: x.start.date() == day, sessions)
    locs = getallsessionlocations(sessions)
    start = min([s.start for s in sessions]+[s.start for s in plenaries]+[s.start for s in globalevents])
    end = max([s.end() for s in sessions]+[s.end() for s in plenaries]+[s.end() for s in globalevents])

    times = list(daterange(start,end,datetime.timedelta(minutes=grain)))

    t = TimeTable()
    t.setCells(locs,times)
    
    for g in globalevents:
        slot = g.start
        while slot < g.end():
            t.addGlobalItem(slot,g)
            slot = slot + datetime.timedelta(minutes=grain)

    for p in plenaries:
        slot = p.start
        while slot < p.end():
            t.addGlobalItem(slot,p)
            slot = slot + datetime.timedelta(minutes=grain)

    for s in sessions:
        for p in Phash[s]: 
            p.xtags=Taghash[p.pk]
            p.faved = str(p.pk) in faves
            slot = p.start
            while slot < p.end:
                t.addItem(s.location,slot,p)
                slot = slot + datetime.timedelta(minutes=grain)

    t.spancols()
    t.spanrows()
    return t

def getallsessionlocations(ss):
    locs = [s.location for s in ss]
    locs = list(set(locs))
    locs.sort(key=lambda x:x.order)
    return locs

def getallpresentationtimes(ss):
    times = []
    for s in ss:
        for p in s.presentation_set.all():
            times.append(s.start+(p.position-1)*datetime.timedelta(minutes=s.talkduration))
    times = list(set(times))
    times.sort()
    return times
