from django.contrib import admin

from . import models

class BookingInline(admin.TabularInline):
    model = models.Booking

class BookingAdmin(admin.ModelAdmin):
    fields=('who','workshop','created','edited')
    readonly_fields=fields

class WorkshopperAdmin(admin.ModelAdmin):
    fields=('user','fullname','credits','spent','credits_left')
    readonly_fields=('spent','credits_left','fullname')
    list_display=('user','fullname','credits','spent','credits_left')
    inlines= [ BookingInline, ]
    pass
class WorkshopAdmin(admin.ModelAdmin):
    fields = ('item','capacity','cost','status','spaces_left')
    readonly_fields = ('spaces_left',)
    list_editable = ('cost','capacity')
    list_display=('item','status','cost','capacity','number_of_bookings')
    inlines= [ BookingInline, ]



admin.site.register(models.Booking,BookingAdmin)
admin.site.register(models.Workshopper,WorkshopperAdmin)
admin.site.register(models.Workshop,WorkshopAdmin)

from secretballot import models as secret
admin.site.register(secret.Vote, admin.ModelAdmin)
