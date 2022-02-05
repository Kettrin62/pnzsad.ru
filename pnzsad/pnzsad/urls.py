from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path("", include("seedlings.urls")),
]

admin.site.site_header = 'Админка PnzSad.ru'
admin.site.site_title = 'Админка'
admin.site.index_title = 'Добро пожаловать в интерфейс администратора!'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL,
    #                       document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS)
