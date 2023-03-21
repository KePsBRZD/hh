from django.shortcuts import render
from django.template import Library
from django.urls import resolve
from django.db.models import Q
from .models import MenuItem, Menu
from django.core.cache import cache

register = Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = resolve(request.path_info).url_name

    # проверяем, есть ли закэшированное меню
    cache_key = f'menu_{menu_name}'
    menu_items = cache.get(cache_key)

    if not menu_items:
        # ищем меню в базе данных
        try:
            menu = Menu.objects.get(name=menu_name)
        except Menu.DoesNotExist:
            menu = None

        # получаем пункты меню и их дочерние элементы из базы данных
        menu_items = MenuItem.objects.filter(
            Q(menu=menu) | Q(menu=None),
            Q(parent=None),
        ).prefetch_related('children')

        # кэшируем результаты запроса на 5 минут
        cache.set(cache_key, menu_items, 300)

    def is_current(url):
        return current_url == url or current_url.startswith(url + '_')

    def process_items(items):
        for item in items:
            item.is_current = is_current(item.url)
            item.has_children = item.children.exists()
            if item.has_children:
                item.children = process_items(item.children.all())
        return items

    menu_items = process_items(menu_items)

    return render(request, 'menu/draw_menu.html', {'menu_items': menu_items, 'current_url': current_url})

def about(request):
    return render(request, 'menu/about.html')