from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import About

EMPTY_VALUE = '-пусто-'


class AboutAdminForm(forms.ModelForm):
    markup = forms.CharField(
        label='Контент',
        widget=CKEditorUploadingWidget(config_name='about_admin')
    )

    class Meta:
        model = About
        fields = '__all__'


class AboutAdmin(admin.ModelAdmin):
    list_display = ('markup',)
    empty_value_display = EMPTY_VALUE
    form = AboutAdminForm


admin.site.register(About, AboutAdmin)
