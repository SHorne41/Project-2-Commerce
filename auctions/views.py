from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm, WatchlistForm


def index(request):
    listingsList = Listing.objects.all()
    activeListings = listingsList.filter(open=True)
    context = {"title": "Active Listings", "listings": activeListings}
    return render(request, "auctions/index.html", context)


def newForm(request):
    newListingForm = ListingForm(initial={'owner': request.user})
    context = {'form': newListingForm}

    return render(request, "auctions/newListing.html", context)


def createNewListing(request):
    if request.method == 'POST':
        user = request.user
        newListingForm = ListingForm(request.POST, initial={'owner': user.id})
        if newListingForm.is_valid():
            newListing = newListingForm.save()      #This line creates a new Listing object, passing in the data from the fields in the form
        else:
            print("Object not created")

    return HttpResponseRedirect(reverse("index"))


def listing_view(request, title):
    currentListing = Listing.objects.get(title=title)           # Listing to be displayed
    listingComments = None

    #Determine if the current listing has any comments
    if Comment.objects.filter(listing=currentListing.pk).exists():
        listingComments = Comment.objects.filter(listing=currentListing.pk)

    isActive = False                                            # Used for context
    isWatching = False                                          # Used for context
    isOwner = False                                             # Used for context
    newWatchlistForm = None                                     #USed for context

    # Is the user currently signed into an account
    if request.user.username != "":
        #Determine if the current user has a watchlist
        if Watchlist.objects.filter(user=request.user).exists():
            userWatchlist = Watchlist.objects.get(user=request.user)    # Current User's watchlist
            #Determine if the item is on the current user's watchlist
            if userWatchlist.listing.filter(title=title):
                isWatching = True
        else:
            newWatchlistForm = WatchlistForm(initial={'user': request.user, 'listing': currentListing})     #Used in the event the current user doesn't have a watchlist
        #Determine if the current user is the owner of the listing
        if currentListing.owner == request.user:
            isOwner = True


    #Determine if the listing is active
    if currentListing.open == True:
        isActive = True

    #Create bidForm/commentForm and pass in context
    newBidForm = BidForm(initial={'user': request.user, 'listing': currentListing.pk})
    newCommentForm = CommentForm(initial={'user': request.user, 'listing': currentListing.pk})

    context = {"listing": currentListing, "comments": listingComments, "watching" : isWatching, "owner": isOwner, "active": isActive, "form": newBidForm, "commentForm": newCommentForm, 'watchlistForm': newWatchlistForm}

    return render(request, "auctions/listing.html", context)

def post_comment(request, title):
    if request.method == 'POST':
        currentListing = Listing.objects.get(title=title)
        newCommentForm = CommentForm(request.POST, initial={'user': request.user.id, 'listing': currentListing.pk})
        newComment = newCommentForm.save()

    return HttpResponseRedirect(reverse("listing", args=[title]))

def place_bid(request, title):
    if request.method == 'POST':
        currentListing = Listing.objects.get(title=title)
        currentBid = currentListing.currentBid
        newBidForm = BidForm(request.POST, initial={'user': request.user.id, 'listing': currentListing.pk})

        if newBidForm.is_valid():
            newBidData = newBidForm.cleaned_data
            #Check to see if new bid is greater than current bid
            if newBidData['bidAmount'] <= currentBid:
                #throw Error
                return HttpResponseRedirect(reverse("listing", args=[title]))  #Remove after error code is inserted
            else:
                currentListing.currentBid = newBidData['bidAmount']
                currentListing.save()
                newBid = newBidForm.save()

    return HttpResponseRedirect(reverse("listing", args=[title]))

def close_listing(request, title):
    #Retrieve the listing and set it to close
    currentListing = Listing.objects.get(title=title)
    currentListing.open = False

    #Retrieve the bids on the current listing to determine the winner'
    listingBids = Bid.objects.filter(listing = currentListing)
    for bid in listingBids:
        bidAmount = bid.bidAmount
        if bidAmount == currentListing.currentBid:
            listingWinner = bid.user

    print(listingWinner)

    #Set the listingWinner as the new owner of the listing
    currentListing.owner = listingWinner
    currentListing.save()

    return HttpResponseRedirect(reverse("listing", args=[title]))

def watchlist(request):
    userID = User.objects.get(username = request.user).pk
    watchListItems = Watchlist.objects.get(user = userID).listing.all()
    context = {"title": "Watchlist", "listings": watchListItems}

    return render(request, "auctions/index.html", context)


def add_to_watchlist(request, title):
    listingItem = Listing.objects.get(title = title).pk
    userID = User.objects.get(username = request.user).pk

    #Determine if the user currently has a watchlist
    if Watchlist.objects.filter(user = userID).exists():
        userWatchlist = Watchlist.objects.get(user = userID)
        userWatchlist.listing.add(listingItem)
    else:
        userWatchlist = WatchlistForm(request.POST, initial={'user': userID, 'listing': listingItem})
        print("creating watchlist")
        if userWatchlist.is_valid():
            newWatchlist = userWatchlist.save()
            print("Watchlist created")
        else:
            print(userWatchlist.errors)


    return HttpResponseRedirect(reverse("watchlist"))

def remove_from_watchlist(request, title):
    listingItem = Listing.objects.get(title = title).pk
    userID = request.user.pk
    userWatchlist = Watchlist.objects.get(user = userID)
    userWatchlist.listing.remove(listingItem)

    return HttpResponseRedirect(reverse("watchlist"))


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
