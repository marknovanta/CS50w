
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user>", views.user_page, name="user_page"),
    path("following", views.following, name="following"),
    path("post_edit/<int:post_id>", views.post_edit, name="post_edit"),
    path("like_dislike/<int:post_id>", views.like_dislike, name="like_dislike")
]
