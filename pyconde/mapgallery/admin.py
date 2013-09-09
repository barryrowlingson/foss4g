from django.contrib import admin

from . import models

class MapAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Map, MapAdmin)
