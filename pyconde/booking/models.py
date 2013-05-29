from django.db import models
from django.contrib.auth.models import User
from pyconde.schedule.models import Session
from django.db.models import Sum
from django.core.exceptions import ValidationError

class Workshop(models.Model):
    WORKSHOP_STATUS = (
        ("OPEN","Open"),
        ("LOCK","Closed")
        )
    item = models.OneToOneField(Session)
    capacity = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    # this is NOT a full/spaces field. Its a lock for admin purposes.
    # - so its for checking in public view code
    status = models.CharField(max_length=4,
                              choices=WORKSHOP_STATUS,
                              default="OPEN")
    def number_of_bookings(self):
        return self.booking_set.count()

    def spaces_left(self):
        return self.capacity - self.number_of_bookings()

    def get_bookings(self):
        return self.booking_set.all()

    def spaceclass(self):
        if self.spaces_left() < 1:
            return "full"
        return "open"

    def overlaps(self,ws):
        r1=self.item
        r2=ws.item
        td = min(r1.end - r2.start, r2.end - r1.start)
        if td.seconds + td.days * 24 * 3600 > 0:
            return True
        else:
            return False
    
    def __unicode__(self):
        return self.item.title

class Workshopper(models.Model):
    """
    Someone who has paid for a workshop. They may not have 
    booked any yet though..
    """
    
    user = models.OneToOneField(User, related_name='workshopper_profile')
    credits = models.PositiveIntegerField("Paid-for credits")
    booked = models.ManyToManyField(Workshop, through="Booking")

    def get_bookings(self):
        return self.booking_set.all()

    def spent(self):
        """
        total booked cost
        """
        total = self.booked.all().aggregate(total=Sum("cost"))["total"]
        if not total:
            total=0
        return total

    def credits_left(self):
        return self.credits - self.spent()

    def __unicode__(self):
        if self.user.first_name and self.user.last_name:
            return u"{0} {1}".format(self.user.first_name, self.user.last_name)
        return self.user.username
    
class Booking(models.Model):
    """
    A booking by a person for a workshop
    """
    who = models.ForeignKey(Workshopper)
    workshop = models.ForeignKey(Workshop)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)


    def clean(self):
        if self.pk:
            return
        ws = self.workshop
        #if ws.status=="LOCK":
        #    raise ValidationError("Workshop booking locked by admin")
        cost = ws.cost
        spaces = ws.spaces_left()
        funds = self.who.credits_left()
        print "checking credit"
        # workshopper must have credit
        if spaces < 1:
            raise ValidationError("No space left in "+str(ws))
        # workshop must have a space
        print "checking space"
        if funds < cost:
            raise ValidationError("Insufficient Funds")


    def save(self, *args, **kwargs):
        print "Saving "+str(self)
        super(Booking, self).save(*args, **kwargs) 

    def __unicode__(self):
        return str(self.who) +  " booked " + str(self.workshop)
