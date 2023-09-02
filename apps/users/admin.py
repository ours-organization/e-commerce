from django.contrib import admin

from apps.users.models import User, UserConfirmation


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_time', 'is_active', 'is_admin', 'is_superuser']


class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ['user','is_confirmed']
admin.site.register(User, UserAdmin)
admin.site.register(UserConfirmation, UserConfirmationAdmin)