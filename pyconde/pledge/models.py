from django.db import models
from django.forms import ModelForm
import django.forms

# Create your models here.

#

STATUS= (
    ("NEW","New entry"),
    ("ACC","Accepted"),
    ("REJ","Rejected"),
    )

DIFFS = (
    ("TRIV","Trivial"),
    ("EASY","Quite Easy"),
    ("TRKY","Tricky"),
    ("IMPO","Impossible!"),
    )

DOBY = (
    ("BF13","Before FOSS4G 2013 starts"),
    ("AF13","Before FOSS4G 2013 ends"),
    ("EN13","This year"),
    ("BF14","Before FOSS4G 2014!"),
    )

    
# pledge model
#  handle: text
#  text of pledge: text
#  difficulty: choice
#  do by: choice
#  contact:
#  accepted: default FALSE
#  create date: date

class AcceptedManager(models.Manager):
    def get_query_set(self):
        return super(AcceptedManager,self).get_query_set().filter(status="ACC")

class Pledge(models.Model):
    text = models.CharField('What is your pledge?',max_length=100)
    handle = models.CharField('Enter a name or nickname for display',max_length=50)
    contact = models.CharField('Optional contact (not for display)',max_length=50, blank=True, null=True)
    
    difficulty = models.CharField('How difficult is this?',
                                  max_length=4,
                                  choices=DIFFS,
                                  default="TRKY")
    status = models.CharField(max_length=4,
                              choices=STATUS,
                              default="NEW")
    doby = models.CharField('When will you do this by?',
                            max_length=4,
                            choices=DOBY,
                            default="EN13")
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    accepted = AcceptedManager()

    def __unicode__(self):
        return u"%s (%s)" % (self.text, self.handle)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from simplemathcaptcha.fields import MathCaptchaField

class PledgeForm(ModelForm):
    captcha = MathCaptchaField()
    class Meta:
        model=Pledge
        fields = ['text','handle','contact','difficulty','doby']
    def clean_text(self):
        data = self.cleaned_data['text']
        if data.lower().startswith("i pledge to "):
            return data
        if data.lower().startswith("we pledge to "):
            return data
        raise django.forms.ValidationError,"Pledge must start 'I pledge to' or 'We pledge to'"
    def __init__(self, *args, **kwargs):
        super(PledgeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-pledgeForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        #self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))

import secretballot
secretballot.enable_voting_on(Pledge)
