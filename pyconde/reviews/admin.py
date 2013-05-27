# -*- encoding: utf-8 -*-
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import models as auth_models

from . import models
from . import utils


def mark_comment_as_deleted(modeladmin, request, queryset):
    queryset.update(deleted=True, deleted_date=datetime.datetime.now(),
        deleted_by=request.user)
mark_comment_as_deleted.short_description = _("Mark comment(s) as deleted")


def export_reviews(modeladmin, request, queryset):
    return HttpResponse(utils.create_reviews_export(queryset).csv, mimetype='text/csv')
export_reviews.short_description = _("Export as CSV")


def export_reviewed_proposals(modeladmin, request, queryset):
    return HttpResponse(utils.create_proposal_score_export(queryset).csv,
        mimetype='text/csv')
export_reviewed_proposals.short_description = _("Export as CSV")


class ProposalMetaDataAdmin(admin.ModelAdmin):
    list_display = ['proposal', 'num_comments', 'num_reviews',
        'latest_activity_date', 'score']
    actions = [export_reviewed_proposals]


admin.site.register(models.ProposalVersion,
    list_display=['original', 'pub_date', 'creator'])
admin.site.register(models.Review,
    list_display=['proposal', 'user', 'rating', 'pub_date'],
    actions=[export_reviews])
admin.site.register(models.Comment,
    list_display=['proposal', 'author', 'pub_date', 'deleted'],
    list_filter=['deleted'],
    actions=[mark_comment_as_deleted])
admin.site.register(models.ProposalMetaData, ProposalMetaDataAdmin)


# Add some more columns and filters to the user admin
class UserAdmin(BaseUserAdmin):
    list_display = list(BaseUserAdmin.list_display) + ['is_superuser', 'is_reviewer']

    def is_reviewer(self, instance):
        return utils.can_review_proposal(instance)
    is_reviewer.boolean = True
    is_reviewer.short_description = u'is reviewer'

admin.site.unregister(auth_models.User)
admin.site.register(auth_models.User, UserAdmin)
