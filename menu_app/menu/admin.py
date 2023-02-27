from django.contrib import admin

from . import models


@admin.register(models.Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'parent', 'menu', )


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('slug', )
