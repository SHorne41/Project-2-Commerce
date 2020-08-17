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
    path("Watchlist", views.watchlist, name="watchlist"),
    path("AddToWatchlist/<str:title>", views.add_to_watchlist, name="add"),
    path("RemoveFromWatchlist/<str:title>", views.remove_from_watchlist, name="remove"),
    path("placeBid/<str:title>", views.place_bid, name="bid"),
    path("closeListing/<str:title>", views.close_listing, name="close"),
    path("postComment/<str:title>", views.post_comment, name="postComment"),
    path("categories", views.categories_view, name="categories"),
    path("showCategory/<str:category>", views.single_category_view, name="showCategory")
]
