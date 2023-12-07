from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newList", views.new_listing, name="new_listing"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/watch", views.watch, name="watch"),
    path("<int:listing_id>/unwatch", views.unwatch, name="unwatch"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("categories/", views.categories, name="categories"),
    path("<str:category>/filter", views.filter, name="filter")
]
