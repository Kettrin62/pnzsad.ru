from django.urls import path

from . import views

urlpatterns = [
    path(
        'seedlings/<slug:category_slug>/',
        views.seedlings,
        name='seedlings_by_category'
    ),
    path('seedlings/', views.seedlings, name='seedlings_all'),
    path('', views.index, name='index'),
]
