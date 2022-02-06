from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path("", views.index_users, name="index_users"),
]
