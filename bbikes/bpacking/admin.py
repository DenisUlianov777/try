from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import *

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    # fields = ['title']
    list_display = ('id', 'title', 'time_create', 'post_photo', 'is_published', 'cat')
    list_display_links = ('id', 'title') # Кликабельные поля
    # ordering = ['title']
    search_fields = ('title', 'cat__name')
    list_editable = ('is_published', )  # Редактирование
    list_filter = ('is_published', 'time_create', 'cat__name')
    filter_horizontal = ['tags']
    list_per_page = 10 # Пагинация
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(description='', ordering='')
    def post_photo(self, bike: Bike):
        if bike.photo:
            return mark_safe(f"<img src='{bike.photo.url}' width=50>")
        return 'Нет фото'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class TagsAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name')
    # list_display_links = ('id', 'name')
    # search_fields = ('name',)
    prepopulated_fields = {"slug": ("tag",)}


# admin.site.register(Bike)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(User, UserAdmin)
