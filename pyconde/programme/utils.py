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
