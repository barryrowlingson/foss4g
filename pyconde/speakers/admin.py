from django.contrib import admin

from . import models


class SpeakerAdmin(admin.ModelAdmin):
    models = models.Speaker
    fields = ("user","affiliation")
    list_display=("user","affiliation")
    list_editable=("user","affiliation")

admin.site.register(models.Speaker,SpeakerAdmin)

