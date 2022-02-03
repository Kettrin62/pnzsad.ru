from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Seedling, Swiper, Comment

EMPTY_VALUE = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'image', 'display_image', 'slug',
    )
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = EMPTY_VALUE

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="65">')

    display_image.__name__ = 'Изображение'


class SeedlingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'image', 'display_image', 'stock',
        'retail_price', 'wholesale_price', 'available', 'created', 'updated',
    )
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = EMPTY_VALUE
    search_fields = ('title',)
    list_filter = ('category', 'available', 'created', 'updated')
    list_editable = ('retail_price', 'wholesale_price', 'stock', 'available')

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="65">')

    display_image.__name__ = 'Изображение'


class SwiperAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'image', 'display_image', 'text', 'created', 'available'
    )
    empty_value_display = EMPTY_VALUE
    list_editable = ('available',)

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="65">')

    display_image.__name__ = 'Изображение'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'seedling', 'author_name', 'text', 'created',
    )
    empty_value_display = EMPTY_VALUE
    search_fields = ('author_name', 'text',)
    list_filter = ('seedling', 'created',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Seedling, SeedlingAdmin)
admin.site.register(Swiper, SwiperAdmin)
admin.site.register(Comment, CommentAdmin)
