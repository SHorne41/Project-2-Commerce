from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist


def index(request):
    listingsList = Listing.objects.all()
    context = {"title": "Active Listings", "listings": listingsList}
    return render(request, "auctions/index.html", context)

def new_listing(request):
    return render(request, "auctions/newListing.html")

def create_listing(request, username):
    Listing.objects.create(
        title = request.POST["title"],
        description = request.POST["description"],
        category = request.POST["category"],
        image = request.POST["image"],
        bid = request.POST["bid"],
        owner = User.objects.get(username=username)
    )

    return HttpResponseRedirect(reverse("index"))

def listing_view(request, title):
    currentListing = Listing.objects.get(title=title)
    context = {"listing": currentListing}

    return render(request, "auctions/listing.html", context)

def watchlist(request, username):
    userID = User.objects.get(username=username).pk
    watchListItems = Watchlist.objects.get(user = userID).listing.all()
    context = {"title": "Watchlist", "listings": watchListItems}

    return render(request, "auctions/index.html", context)

def add_to_watchlist(request, username, title):
    listingItem = Listing.objects.get(title = title).pk
    userID = User.objects.get(username=username).pk
    userWatchlist = Watchlist.objects.get(user = userID)

    userWatchlist.listing.add(listingItem)
    return HttpResponseRedirect(reverse("watchlist", args=[username]))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
