from django.contrib import admin
from .models import Entry
from django.conf.urls import url


class Log(admin.ModelAdmin):
    """
    How the log is viewed on the admin site
    """

    readonly_fields = ['time','user','trigger', 'activity']
    list_display = ('time', 'user', 'activity', 'trigger')
    list_display_links = None

    list_filter = (
        ('time', admin.DateFieldListFilter),
        'activity',
    )

    search_fields = ['user']

    def has_add_permission(self, request):
        return False

    # Comment this out to display the check boxes
    # so that admins can delete entries from the log
    actions = None


admin.site.register(Entry, Log)
