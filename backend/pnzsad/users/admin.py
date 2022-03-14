from django.contrib import admin

from .models import User

EMPTY_VALUE = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'is_wholesaler',
        'date_joined', 'is_active',
    )
    empty_value_display = EMPTY_VALUE
    search_fields = ('first_name', 'last_name', 'email',)
    list_filter = ('is_active', 'is_wholesaler',)
    list_editable = ('is_active', 'is_wholesaler',)


admin.site.register(User, UserAdmin)
