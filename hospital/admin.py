from django.contrib import admin

# Register your models here.
from .models import actionHistory

class actionHistoryAdmin(admin.ModelAdmin):
    list_display = ('action', 'observation')

admin.site.register(actionHistory, actionHistoryAdmin)