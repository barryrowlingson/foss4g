import pytz
from pytz import timezone
from icalendar import Calendar,Event
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from datetime import datetime

def calFromEvents(events):
    """ list of events with start/end/title/insession/presenter attributes """
    
    london =timezone("Europe/London")
    cal=Calendar()
    cal.add('prodid','-//FOSS4G Calendar//2013.foss4g.org//')
    cal.add('version','2.0')
    for event in events:
        url = "http://2013.foss4g.org"+reverse('view-presentation',kwargs={'presentation_pk': event.pk})
        
        e = Event()
        e.add('summary',u"%s (%s)" % (event.title,event.presenter.name))
        e.add('description',event.desc)
        e.add('url',url)
        e.add('dtstart', london.localize(event.start))
        e.add('dtend', london.localize(event.end))
        e.add('location', event.insession.location)
        e.add('dtstamp', datetime(2013,8,1,0,0,0,tzinfo=pytz.utc))
        e['uid'] = slugify(u"%s-%s" % (event.title , event.presenter.name))
        cal.add_component(e)
    return cal

