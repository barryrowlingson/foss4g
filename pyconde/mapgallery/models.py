from django.db import models

# Create your models here.

class Map(models.Model):
    row = models.IntegerField("row in spreadsheet")
    author = models.CharField(max_length=200)
    org = models.CharField(max_length=200, blank=True)
    assoc = models.TextField()
    tellus = models.TextField()
    category = models.CharField(max_length=100)
    mapformat = models.CharField(max_length=10)
    fullname = models.CharField(max_length=100, blank=True)
    URL = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=100)
    vcount = models.IntegerField("voting count",default=0)
    
    def __unicode__(self):
        return u"%s: %s, by %s (%s)" % (self.row, self.title, self.author, self.org)

import secretballot
secretballot.enable_voting_on(Map)
