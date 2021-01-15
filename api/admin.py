from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import User


class UserAdmin(ImportExportModelAdmin):
    list_display = (
        'username',
        'role',
        'email',
        'confirmation_code',
        'bio',
        'first_name',
        'last_name'
    )
    search_fields = ("last_name",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
