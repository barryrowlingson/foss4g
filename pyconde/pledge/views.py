#
# pledge system
#

#

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from . import models

def pledgelist(request):
    pledges = models.Pledge.objects.filter(status="ACC")
    context={'pledges': pledges}
    return render_to_response("pledge/index.html",
                              context,
                              context_instance=RequestContext(request)
                              )

from django.core.urlresolvers import reverse
from . import models
from django.contrib import messages

def pledgecreate(request):
    if request.method == 'POST': # If the form has been submitted...
        form = models.PledgeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
            messages.add_message(request, messages.INFO,'Pledge will appear soon!')
            return HttpResponseRedirect(reverse('pledge-list')) # Redirect after POST
    else:
        form = models.PledgeForm() # An unbound form

    return render(request, 'pledge/create.html', {
        'form': form, 'helper': form.helper,
    })
