from django.contrib import admin

from forms import PeriodicTaskForm
from .models import User, ScraperTask, ScrapedData, ScraperLog, ScraperScript
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_celery_beat.admin import PeriodicTaskAdmin
from django_celery_beat.models import PeriodicTask


class CustomPeriodicTaskAdmin(admin.ModelAdmin):
    form = PeriodicTaskForm 
    fieldsets=(
        (None, {'fields': ('name', 'task', 'interval', 'crontab', 'enabled')}),
    )

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(ScraperScript)
admin.site.register(ScraperTask)
admin.site.register(ScrapedData)
admin.site.register(ScraperLog)

# Unregister the default PeriodicTask admin and register the custom one
admin.site.unregister(PeriodicTask)
admin.site.register(PeriodicTask, CustomPeriodicTaskAdmin)

