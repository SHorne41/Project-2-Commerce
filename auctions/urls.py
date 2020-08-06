from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.new_listing, name="new"),
    path("createListing", views.create_listing, name="create"),
    path("<str:title>Listing", views.listing_view, name="listing")
]
