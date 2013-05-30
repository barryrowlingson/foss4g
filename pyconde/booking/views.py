# Create your views here.

from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from pyconde.accounts.models import Profile

from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

from .models import Workshop, Workshopper
from . import utils

import sys

def index(request):
    context  = {
        "workshops":Workshop.objects.order_by("item__start"),
        }
    return render_to_response("booking/booking_index.html",
                              context,
                              context_instance=RequestContext(request))


def book(request):
    if not request.user.is_authenticated():
        return redirect('login?next=%s' % request.path)
    if request.method == "POST":
        print "got a POST"
        messages.add_message(request, messages.INFO, 'Got a POST.')
        # handle the action - book or unbook
        print request.POST['workshop']
        print request.POST['action']
        if request.POST['action']=="book":
            msg = utils.bookSession(request.user, request.POST['workshop'])
            messages.add_message(request, messages.INFO,msg)
        elif request.POST['action']=="unbook":
            msg = utils.unbookSession(request.user, request.POST['workshop'])
            messages.add_message(request, messages.INFO,msg)
        else:
            messages.add_message(request,messages.INFO, "Unrecognised action")
        return HttpResponseRedirect("book")
    else:
        pass

    workshopper = request.user.workshopper_profile
    credits_left = workshopper.credits_left()
    
    workshops = Workshop.objects.select_related().order_by("item__start")

    for w in workshops:
        w.spaceclassX = w.spaceclass()

    booked = workshopper.booked.all()

    utils.addstates(workshopper, booked,  workshops)

    context = {
        "funds": credits_left,
        "workshops": workshops
        }
    return render_to_response("booking/booking_book.html",
                              context,
                              context_instance=RequestContext(request))

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("book")
            else:
                messages.add_message(request,messages.INFO, "Account disabled")
                return HttpResponseRedirect("login")
        else:
            messages.add_message(request,messages.INFO, "Invalid login/pass")
            return HttpResponseRedirect("login")
    else:
        return render_to_response("booking/login.html",
                                  {},
                                  context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(".")

@permission_required('booking.add_booking')
def add_workshopper(request):
    if request.method == "POST":
        newU = User(
            username = request.POST['user'],
            password = make_password(request.POST['pass']),
            email = request.POST['email'],
            first_name = request.POST['firstname'],
            last_name = request.POST['lastname']
            )
        try:
            newU.save()
        except:
            e = str(sys.exc_info()[1])
            html = "<html><body><p>Error: %s creating User</p></body></html>" % e
            return HttpResponse(html)
        credits = int(request.POST['credits'])
        newP = Profile(user=newU)
        newP.save()
        newW = Workshopper(user=newU, credits=credits)
        newW.save()
        messages.add_message(request,messages.INFO, "Workshopper created")
        return HttpResponseRedirect("")
    return render_to_response("booking/add_ws.html",{},context_instance=RequestContext(request))
