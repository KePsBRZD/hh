from django import template
from django.urls import resolve

from menu.models import Menu, MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url_name = resolve(request.path_info).url_name

    # Получаем меню по имени
    menu = Menu.objects.filter(name=menu_name).first()
    if menu is None:
        return ''

    # Получаем элементы меню первого уровня
    menu_items = MenuItem.objects.filter(menu=menu, parent=None).order_by('position').prefetch_related('children')

    # Рекурсивно обрабатываем элементы меню
    def process_items(items):
        for item in items:
            item.is_current = current_url_name == item.url_name
            item.has_children = item.children.exists()
            if item.has_children:
                item.children = process_items(item.children.all())
        return items

    menu_items = process_items(menu_items)

    return {'menu_items': menu_items}