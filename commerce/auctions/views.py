from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment
from .forms import NewListingForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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



@login_required(login_url="login")
def new_listing(request):
    if request.method == "GET":
        return render(request, "auctions/new_listing.html", {
            "form": NewListingForm()
        })
    else:
        form = NewListingForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            l = Listing(user=user, title=title, category=category, image=image, description=description, starting_bid=starting_bid)
            l.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html", {
            "message": "Form not valid"
        })


def listing(request, id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=id)
        comments = Comment.objects.filter(listing=id)
        if request.user.is_authenticated:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "watchlist": request.user.watchlist.all(),
                "user": request.user,
                "comments": comments
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments
            })

@login_required(login_url="login")
def watchlist(request):
    print(request.user.watchlist)
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all()
    })

@login_required(login_url="login")
def watch(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        user.watchlist.add(listing)
        user.save()
        return HttpResponseRedirect(reverse("watchlist"))

@login_required(login_url="login")
def unwatch(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        user.watchlist.remove(listing)
        user.save()
        return HttpResponseRedirect(reverse("watchlist"))

@login_required(login_url="login")
def bid(request, listing_id):
    if request.method == "POST":
        amount = request.POST["amount"]
        listing = Listing.objects.get(pk=listing_id)
        comments = Comment.objects.filter(listing=listing_id)
        if amount:
            amount = float(amount)
            listing = Listing.objects.get(pk=listing_id)
            if listing.status == "open":
                if amount < listing.starting_bid:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "watchlist": request.user.watchlist.all(),
                        "comments": comments,
                        "message": "ERROR: Amount must be minimum the current price"
                    })  
                else:
                    listing.starting_bid = amount
                    listing.status = "auction"
                    user = User.objects.get(pk=request.user.id)
                    listing.winner = user.username
                    b = Bid(user=user, listing=listing, amount=amount)
                    b.save()
                    listing.save()
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "watchlist": request.user.watchlist.all(),
                        "message": "Bid success"
                    })

            elif listing.status == "auction":
                if amount <= listing.starting_bid:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "watchlist": request.user.watchlist.all(),
                        "comments": comments,
                        "message": "ERROR: Amount must be higher than the current price"
                    })  
                else:
                    listing.starting_bid = amount
                    user = User.objects.get(pk=request.user.id)
                    listing.winner = user.username
                    b = Bid(user=user, listing=listing, amount=amount)
                    b.save()
                    listing.save()
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "watchlist": request.user.watchlist.all(),
                        "comments": comments,
                        "message": "Bid success"
                    })
        else:
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": request.user.watchlist.all(),
            "comments": comments,
            "message": "ERROR: Amount not valid"
        })

@login_required(login_url="login")
def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.status = "closed"
    listing.save()
    comments = Comment.objects.filter(listing=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": request.user.watchlist.all(),
        "comments": comments,
        "message": "Auction closed"
    })

@login_required(login_url="login")
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        content = request.POST["comment"]
        comment = Comment(user=user, listing=listing, content=content)
        comment.save()
        comments = Comment.objects.filter(listing=listing_id)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def categories(request):
    categories = list()
    listings = Listing.objects.all()
    for listing in listings:
        category = listing.category
        if category not in categories:
            categories.append(category)
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def filter(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings
    }) 