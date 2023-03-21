from django.contrib import admin
from .models import Menu, MenuItem

class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 0

class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'position', 'parent', 'menu')

admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)