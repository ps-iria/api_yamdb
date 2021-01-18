from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Genre, Category, Title, User, Review


class CategoryAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'


class GenreAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'


class TitleAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
        'get_genre'
    )
    empty_value_display = '-пусто-'


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


class ReviewAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'author',
        'title',
        'text',
        'score',
        'pub_date'
    )
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
