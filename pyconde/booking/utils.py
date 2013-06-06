
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
        return "Booked "+str(w)
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
    return "Removed booking of "+str(w)
    
from random import sample
def randompass():
    letters = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    l1 = "".join(sample(letters,3))
    n = "".join(sample(numbers,3))
    l2 = "".join(sample(letters,3))
    return l1+n+l2


import ucsv as csv
def readcsv(filepath):
    with open(filepath, 'rb') as f:
        reader = csv.reader(f)
        reader.next() # skip header
        for row in reader:
            yield row

def checkrecords(recordlist):
    for rec in recordlist:
        if len(rec) != 5:
            raise ValueError,"Incorrect length for ",rec
        if rec[0].strip()=="":
            raise ValueError, "No First name"
        if rec[1].strip()=="":
            raise ValueError,"No Last name"
        if rec[3].strip()=="":
            raise ValueError,"No email"
        hrs = rec[4].strip()
        is8 = hrs=="8 hour"
        is16 = hrs=="16 hour"
        if not is8 and not is16:
            raise ValueError, "Booking duration is "+str(hrs)
        
