from django.contrib import admin

from . import models


# class WorkshopAdmin(admin.ModelAdmin):
#     fields = ('item','capacity','cost','status','spaces_left')
#     readonly_fields = ('spaces_left',)
#     list_editable = ('cost','capacity')
#     list_display=('item','status','cost','capacity','number_of_bookings')
#     inlines= [ BookingInline, ]


class PSessionAdmin(admin.ModelAdmin):
    pass

class PresentationAdmin(admin.ModelAdmin):
    filter_horizontal = ('copresenter',)
    list_display=('title','presenter','insession')
    list_filter = ('insession',)
    search_fields = ('presenter__name','title',)

class PersonAdmin(admin.ModelAdmin):
    list_display=('name','affiliation','email')
    list_editable=('affiliation','email')
    search_fields=('name','affiliation','email')

admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Presentation,PresentationAdmin) 
admin.site.register(models.PSession, PSessionAdmin)
admin.site.register(models.Keynote, admin.ModelAdmin)
