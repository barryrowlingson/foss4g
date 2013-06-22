from django.contrib import admin

from . import models


# class WorkshopAdmin(admin.ModelAdmin):
#     fields = ('item','capacity','cost','status','spaces_left')
#     readonly_fields = ('spaces_left',)
#     list_editable = ('cost','capacity')
#     list_display=('item','status','cost','capacity','number_of_bookings')
#     inlines= [ BookingInline, ]



admin.site.register(models.Person, admin.ModelAdmin)
admin.site.register(models.Presentation,admin.ModelAdmin) 
admin.site.register(models.PSession, admin.ModelAdmin)
admin.site.register(models.Keynote, admin.ModelAdmin)
