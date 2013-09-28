#
# pledge system
#

#

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.mail import send_mail
from django.conf import settings 

from . import models

def pledgelist(request):
    pledges = models.Pledge.objects.filter(status="ACC").order_by("?")[:10] # dont use accepted Manager
    context={'pledges': pledges}
    return render_to_response("pledge/index.html",
                              context,
                              context_instance=RequestContext(request)
                              )

def pledgeall(request):
    """ show all pledges for after closing date """
    pledges = models.Pledge.objects.filter(status="ACC")
    context={'pledges': pledges}
    return render_to_response("pledge/pledgeall.html",
                              context,
                              context_instance=RequestContext(request)
                              )
   


from django.core.urlresolvers import reverse
from . import models
from django.contrib import messages
import urlparse

def pledgecreate(request):
    if request.method == 'POST': # If the form has been submitted...
        form = models.PledgeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            pledge = form.save()
            change_url = reverse('admin:pledge_pledge_change', args=(pledge.id,))
            o = urlparse.urlparse(request.build_absolute_uri())
            change_url = urlparse.urlunparse(urlparse.ParseResult(o.scheme,o.netloc,change_url,None,None,None))
            messages.add_message(request, messages.INFO,"<strong>Thanks!</strong> We'll check that out and put it up!")
            msg = """
New Pledge: "%s" from "%s" (%s) \n %s
""" % (form.cleaned_data['text'],form.cleaned_data['handle'],form.cleaned_data['contact'],change_url)
#
#
            send_mail("New FOSS4G Pledge",msg,"noreply@2013.foss4g.org",settings.PLEDGE_NOTIFY,fail_silently=False)
            return HttpResponseRedirect(reverse('pledge-list')) # Redirect after POST
    else:
        form = models.PledgeForm() # An unbound form

    return render(request, 'pledge/create.html', {
        'form': form, 'helper': form.helper,
    })
