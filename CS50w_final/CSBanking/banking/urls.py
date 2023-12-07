from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("get_balance/", views.get_balance, name="get_balance"),
    path("get_contacts/", views.get_contacts, name="get_contacts"),
    path("add_contact/", views.add_contact, name="add_contact"),
    path("remove_contact/<int:contact_id>", views.remove_contact, name="remove_contact"),
    path("transfer/", views.transfer, name="transfer"),
    path("get_transactions/", views.get_transactions, name="get_transactions"),
    path("get_user/", views.get_user, name="get_user"),
    path("add_cash/", views.add_cash, name="add_cash")
]