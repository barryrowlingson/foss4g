
from .models import Workshop, Workshopper, Booking

def workshopstates(workshopper, booked, workshops):
    states={}
    return [(w.pk,workshopstate(workshopper, booked, w)) for w in workshops]

def addstates(workshopper, booked, workshops):
    for w in workshops:
        w.state=workshopstate(workshopper,booked,w)


def workshopstate(workshopper, booked, w):
        if w in booked:
            print "booked ",w.pk
            return "booked"
        if w.status=="LOCK":
            return "locked"
        if w.cost > workshopper.credits_left():
            return "expensive"
        if w.spaces_left() < 1:
            return "full"
        for b in booked:
            if b.item.start and w.item.start:
                if w.overlaps(b):
                    return "conflicts"
        return "bookable"


def bookSession(user, workshopid):
    workshopper = user.workshopper_profile
    booked = workshopper.booked.all()
    w = Workshop.objects.get(pk=workshopid)
    code = workshopstate(workshopper, booked, w)
    if code == "bookable":
        b = Booking(who=workshopper, workshop=w)
        b.save()
        return "Booked"
    else:
        return "Problem booking session: %s" % code
    
def unbookSession(user, workshopid):
    workshopper = user.workshopper_profile
    w = Workshop.objects.get(pk=workshopid)

    b = Booking.objects.filter(who=workshopper,workshop=w)
    if len(b) == 0:
        return "Booking not found"
    if len(b) > 1:
        return "Error - multiple identical bookings found"
    b=b[0]
    b.delete()
    return "Removed booking"
    
