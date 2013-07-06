# Create your views here.
#
#

#
# pledge system
#

#
from django.shortcuts import render_to_response
from django.template import RequestContext

def pledgelist(request):
    context={}
    return render_to_response("pledge/index.html",
                              context,
                              context_instance=RequestContext(request)
                              )
