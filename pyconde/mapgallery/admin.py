from django.contrib import admin

from . import models

class MapAdmin(admin.ModelAdmin):
    list_display=('sID','title','author','directory','competition','format')
    pass

class PrizeAdmin(admin.ModelAdmin):
    list_display=('title','position','winner','runnerup')
    list_editable=('position','winner','runnerup')
    ordering=('position',)
admin.site.register(models.Prize,PrizeAdmin)

admin.site.register(models.Map, MapAdmin)
