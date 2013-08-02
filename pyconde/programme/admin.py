from django.contrib import admin

from . import models


# class WorkshopAdmin(admin.ModelAdmin):
#     fields = ('item','capacity','cost','status','spaces_left')
#     readonly_fields = ('spaces_left',)
#     list_editable = ('cost','capacity')
#     list_display=('item','status','cost','capacity','number_of_bookings')
#     inlines= [ BookingInline, ]

class PresInline(admin.StackedInline):
    model = models.Presentation
    fields = ('copresenter','desc','position')
    readonly_fields = ('copresenter','desc','position')
    ordering = ('position',)
    can_delete = False
    extra = 0

class PSessionAdmin(admin.ModelAdmin):
    inlines = [ 
        PresInline,
        ]
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

class ItemInline(admin.StackedInline):
    model=models.PlenaryItem
    ordering = ('position',)
    extra = 1

class PlenarySessionAdmin(admin.ModelAdmin):
    list_display=('pk','title','start','duration')
    list_editable=('title','start','duration')
    inlines = [ItemInline,]

class PlenaryItemAdmin(admin.ModelAdmin):
    list_display=('pk','title','session','position','duration','details','link')
    list_editable=('title','session','position','duration','details','link')
    

class CWAdmin(admin.ModelAdmin):
    filter_horizontal = ('copresenter',)

admin.site.register(models.CWorkshop,CWAdmin)

admin.site.register(models.PlenaryItem, PlenaryItemAdmin)

admin.site.register(models.PlenarySession, PlenarySessionAdmin)

admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Presentation,PresentationAdmin) 
admin.site.register(models.PSession, PSessionAdmin)
admin.site.register(models.Keynote, admin.ModelAdmin)

admin.site.register(models.GlobalEvent, admin.ModelAdmin)
admin.site.register(models.SpecialEvent, admin.ModelAdmin)
