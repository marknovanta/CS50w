from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show, name="show"),
    path("np/", views.new_page, name="new_page"),
    path("ep/", views.edit_page, name="edit_page"),
    path("random/", views.random_page, name="random")
]
