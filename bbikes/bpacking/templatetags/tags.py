from django import template
from bpacking.models import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

register = template.Library()

@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('bpacking/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('bpacking/list_tags.html')
def show_all_tags():
    return {"tags": Tags.objects.all()}
