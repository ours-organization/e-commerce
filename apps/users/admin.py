from django.contrib import admin

from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_time', 'is_admin', 'is_superuser']


admin.site.register(User, UserAdmin)
