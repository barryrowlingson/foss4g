# Create your views here.

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib import messages

from django.template import RequestContext

from .models import Workshop

def index(request):
    context  = {
        "workshops":Workshop.objects.order_by("item__start"),
        }
    return render_to_response("booking/booking_index.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
def book(request):
    if request.method == "POST":
        print "got a POST"
        messages.add_message(request, messages.INFO, 'Got a POST.')
        # handle the action - book or unbook
        print request.POST['workshop']
        print request.POST['action']
    else:
        pass

    workshopper = request.user.workshopper_profile
    credits_left = workshopper.credits_left()
    

    workshops = Workshop.objects.order_by("item__start")
    context = {
        "funds": credits_left,
        "workshops": workshops
        }
    return render_to_response("booking/booking_book.html",
                              context,
                              context_instance=RequestContext(request))
