from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('email','first_name','last_name','role','university','is_active')
    list_filter=('role','university','is_active')
    search_fields=('email','first_name','last_name')

for model in [Club,Society,Membership,Follow,NewsPost,Event,EventRegistration,MediaItem,AcademicResource,Notification,Cafe,Sport,Match,SiteSetting]:
    admin.site.register(model)
