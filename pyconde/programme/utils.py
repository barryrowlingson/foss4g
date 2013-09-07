#!/bin/env
#
# utilities
#

from pyconde.programme import models
from django.db.models import Count

def useless():
    
    rolecounts = models.Person.objects.annotate(
        num_pres = Count("presenter", distinct=True)
        ).annotate(
        num_cops=Count("presentation",distinct=True)
        ).annotate(
        num_chair = Count("chairperson",distinct=True)
        ).annotate(
        num_help = Count("helper",distinct=True)
        )

    for p in rolecounts:
        p.total = p.num_pres + p.num_cops + p.num_chair + p.num_help
    return rolecounts

import datetime

def nice_repr(timedelta, display="long", sep=", "):
    """
    Turns a datetime.timedelta object into a nice string repr.
    
    display can be "minimal", "short" or "long" [default].
    
    >>> from datetime import timedelta as td
    >>> nice_repr(td(days=1, hours=2, minutes=3, seconds=4))
    '1 day, 2 hours, 3 minutes, 4 seconds'
    >>> nice_repr(td(days=1, seconds=1), "minimal")
    '1d, 1s'
    """
    
    assert isinstance(timedelta, datetime.timedelta), "First argument must be a timedelta."
    
    result = []
    
    weeks = timedelta.days / 7
    days = timedelta.days % 7
    hours = timedelta.seconds / 3600
    minutes = (timedelta.seconds % 3600) / 60
    seconds = timedelta.seconds % 60
    
    if display == "sql":
        days += weeks * 7
        return "%i %02i:%02i:%02i" % (days, hours, minutes, seconds)
    elif display == 'minimal':
        words = ["w", "d", "h", "m", "s"]
    elif display == 'short':
        words = [" wks", " days", " hrs", " min", " sec"]
    else:
        words = [" weeks", " days", " hours", " minutes", " seconds"]
    
    values = [weeks, days, hours, minutes, seconds]
    
    for i in range(len(values)):
        if values[i]:
            if values[i] == 1 and len(words[i]) > 1:
                result.append("%i%s" % (values[i], words[i].rstrip('s')))
            else:
                result.append("%i%s" % (values[i], words[i]))
    
    return sep.join(result)
