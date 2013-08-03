from models import Presentation,PSession,Person,PlenarySession,CWorkshop

from timetabling import TimeTable

import datetime

def daterange(start_datetime, end_datetime, delta):
    current = start_datetime
    while current < end_datetime:
        yield current
        current = current + delta

def time1(day, grain=30):
    #presentations = Presentation.objects.all()

    #1 add the global events
    #2 add the plenaries
    #3 add the sessions

    sessions = PSession.objects.filter(start__contains=day)
    #sessions = filter(lambda x: x.start.date() == day, sessions)
    locs = getallsessionlocations(sessions)
    start = min([s.start for s in sessions])
    end = max([s.end() for s in sessions])

    times = list(daterange(start,end,datetime.timedelta(minutes=grain)))

    t = TimeTable()
    t.setCells(locs,times)
    
    for s in sessions:
        for p in s.presentation_set.all():
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
