from django.contrib import admin

from apps.users.models import CustomUser, Saved


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'is_active']
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Saved)