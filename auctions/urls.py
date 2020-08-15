from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newForm, name="new"),
    path("createListing", views.createNewListing, name="create"),
    path("<str:title>Listing", views.listing_view, name="listing"),
    path("<str:username>Watchlist", views.watchlist, name="watchlist"),
    path("AddToWatchlist/<str:username>/<str:title>", views.add_to_watchlist, name="add"),
    path("RemoveFromWatchlist/<str:title>", views.remove_from_watchlist, name="remove")
]
