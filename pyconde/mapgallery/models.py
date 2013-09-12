from django.db import models

# Create your models here.

class Map(models.Model):
    sID = models.IntegerField("row in spreadsheet")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    directory = models.CharField(max_length=30)    
    org = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    competition = models.CharField(max_length=100)
    format = models.CharField(max_length=10)
    URL = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return u"%s: %s, by %s" % (self.sID, self.title, self.author)

import secretballot
secretballot.enable_voting_on(Map)
