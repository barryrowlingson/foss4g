
def workshopstates(workshopper, booked, workshops):
    states={}
    return [(w.pk,workshopstate(workshopper, booked, w)) for w in workshops]


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


