from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
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



def new_listing(request):
    if request.method == "GET":
        return render(request,"auctions/listing.html")
    else:
        a = request.POST
        b = Listing(
            title = a["title"],
            description = a["description"],
            img_url = a["img_url"],
            category = a["category"],
            starting_bid = a["starting_bid"],
            user = request.user
            )
        b.save()
        return render(request, "auctions/succes.html", {
            'message': "The list was created successfully!"
        })


def list(request, id1):
    if request.method == "GET":
        listing = Listing.objects.filter(id = id1).first()
        watchlist = None
        if (request.user.is_authenticated):
            watchlist = Watchlist.objects.filter(listing=listing, user=request.user).first()
        comment = listing.comment_set.all()
        a = listing.maximum_bid()
        b = listing.starting_bid
        print(a)
        if a["bid__max"] is None:
            a["bid__max"] = b
        print(y)
        return render(request, "auctions/list.html", {
            "listing": listing,
            "comments": comment,
            "watchlist": watchlist,
            "maximum_bid": a
        })
