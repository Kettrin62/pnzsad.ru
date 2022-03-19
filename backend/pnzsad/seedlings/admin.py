from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Comment, Seedling, Swiper

EMPTY_VALUE = '-пусто-'


class SeedlingAdminForm(forms.ModelForm):
    full_description = forms.CharField(
        label='Полное описание',
        widget=CKEditorWidget(config_name='seedlint_admin')
    )

    class Meta:
        model = Seedling
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_image', 'display_order'
    )
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = EMPTY_VALUE
    list_editable = ('display_order',)

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="65" height="65">')

    display_image.__name__ = 'Изображение'


class SeedlingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'display_image', 'stock',
        'retail_price', 'wholesale_price', 'available', 'display_order'
    )
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = EMPTY_VALUE
    search_fields = ('title',)
    form = SeedlingAdminForm
    list_filter = ('category', 'available', 'created', 'updated')
    list_editable = (
        'retail_price', 'wholesale_price', 'stock',
        'available', 'display_order'
    )

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="65"  height="65">')

    display_image.__name__ = 'Изображение'


class SwiperAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_image', 'text', 'display_order', 'available',
    )
    empty_value_display = EMPTY_VALUE
    list_editable = ('available', 'display_order', 'text')

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="65"  height="65">')

    display_image.__name__ = 'Изображение'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'seedling', 'author_name', 'text', 'created',
    )
    empty_value_display = EMPTY_VALUE
    search_fields = ('author_name', 'text',)
    list_filter = ('seedling', 'created',)
    list_editable = ('text',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Seedling, SeedlingAdmin)
admin.site.register(Swiper, SwiperAdmin)
admin.site.register(Comment, CommentAdmin)
