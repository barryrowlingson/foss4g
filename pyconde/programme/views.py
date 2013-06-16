
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

def index(request):
    context = {}
    return render_to_response("programme/index.html",
                              context,
                              context_instance=RequestContext(request))

def workshops(request):
    context = {}
    return render_to_response("programme/workshops.html",
                              context,
                              context_instance=RequestContext(request))

def view_workshop(request, workshop_pk):
    context = {}
    return render_to_response("programme/view_workshop.html",
                              context,
                              context_instance=RequestContext(request))

def view_presentation(request, presentation_pk):
    context = {}
    return render_to_response("programme/view_presentation.html",
                              context,
                              context_instance=RequestContext(request))


 
