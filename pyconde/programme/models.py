from django.db import models

# Create your models here.
from pyconde.conference import models as conference_models
from pyconde.tagging import TaggableManager
from tinymce import models as tinymce_models

import datetime

class Person(models.Model):
    name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    contact = models.TextField(blank=True)
    biog = tinymce_models.HTMLField(blank=True)    
    notes = models.TextField("Committee use only",blank=True)

    def __unicode__(self):
        return self.name

class PSession(models.Model):
    chair = models.ForeignKey(Person, blank=True, null=True,related_name="chairperson")
    helper = models.ForeignKey(Person, blank=True, null=True,related_name="helper")
    start = models.DateTimeField()
    location = models.ForeignKey(conference_models.Location,blank=True, null=True)
    talkduration = models.IntegerField("minutes per talk")
    slotcount = models.IntegerField("how many talks in this?")
    title = models.CharField(max_length=200)
    tags = TaggableManager(blank=True)
    notes = models.TextField("Committee use only",blank=True)

    def end(self):
        return self.start + datetime.timedelta(minutes=self.talkduration)*self.slotcount

    def __unicode__(self):
        if self.location:
            return u"%s: %s talks in %s at %s " % (self.title,self.slotcount,self.location, self.start)
        else:
            return u"%s: %s talks at %s in unassigned room" % (self.title,self.slotcount,self.start)


class Presentation(models.Model):
    presenter = models.ForeignKey(Person, related_name="presenter")
    copresenter = models.ManyToManyField(Person, blank=True, null=True)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    abstract = tinymce_models.HTMLField()    
    insession = models.ForeignKey(PSession, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    notes = models.TextField("Committee use only",blank=True)
    cancelled = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.presenter)

class Keynote(models.Model):
    speaker = models.ForeignKey(Person)
    title = models.CharField(max_length=200)
    abstract = tinymce_models.HTMLField()
    notes = models.TextField("Committee use only",blank=True)
    cancelled = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.speaker)

