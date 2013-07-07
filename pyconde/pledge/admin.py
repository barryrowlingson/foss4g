from django.contrib import admin

from . import models

class PledgeAdmin(admin.ModelAdmin):
    save_on_top=True
    list_display=('pk','text','handle','status')
    list_editable=('text','handle','status')
    ordering = ('-status',)
    pass

admin.site.register(models.Pledge, PledgeAdmin)

