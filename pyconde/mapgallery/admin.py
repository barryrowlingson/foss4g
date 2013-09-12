from django.contrib import admin

from . import models

class MapAdmin(admin.ModelAdmin):
    list_display=('sID','title','author','directory','competition','format')
    pass

admin.site.register(models.Map, MapAdmin)
