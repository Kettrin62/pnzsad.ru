from django.urls import path

from . import views

app_name = 'seedlings'


urlpatterns = [
    path(
        'seedlings/<str:category_slug>/<str:seedling_slug>/',
        views.seedling_page,
        name='seedling_page'
    ),
    path(
        'seedlings/<slug:category_slug>/',
        views.seedlings,
        name='seedlings_by_category'
    ),
    path('seedlings/', views.seedlings, name='seedlings_all'),
    path('', views.index, name='index'),
]
