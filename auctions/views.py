from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bids, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        'catalogs': Listing.objects.all()
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


def new_item(request):
    if request.method == "GET":
        return render(request,"auctions/new_item.html")
    else:
        li = Listing(
            name = request.POST["name"],
            description = request.POST["description"],
            img_url = request.POST["img_url"],
            category = request.POST["category"],
            starting_bid = request.POST["starting_bid"],
            owner = request.user
            )
        li.save()
        return render(request, "auctions/success.html", {
            'message': "The List Was Created Successfully!"
        })


def item(request, id1):
    if request.method == "GET":
        catalog = Listing.objects.filter(id = id1).first()
        watchlist = None
        if (request.user.is_authenticated):
            watchlist = Watchlist.objects.filter(catalog=catalog, user=request.user).first()
        comment = catalog.comment_set.all()
        a = catalog.maximum_bid()
        b = catalog.starting_bid
        print(a)
        if a["bid__max"] is None:
            a["bid__max"] = b
        print(b)
        return render(request, "auctions/item.html", {
            "catalog": catalog,
            "comments": comment,
            "watchlist": watchlist,
            "maximum_bid": a
        })


def new_bid(request, id):
    if request.method == "POST":
        bid = request.POST["bid"]
        catalog = Listing.objects.get(pk = id)
        bi = Bids(catalog = Listing.objects.get(pk = id), user = request.user, bid = bid)
        bi.save()
        catalog.maximum_bid = bi
        catalog.new_owner = bi.user
        catalog.save()
        return HttpResponseRedirect(reverse("item", kwargs = {"id1": id}))


def close_bid(request, id):
    catalog = Listing.objects.get(pk = id)
    catalog.active = False
    catalog.save()
    return HttpResponseRedirect(reverse("item", kwargs = {"id1": id}))


def comment(request):
    if request.method == "POST":
        text = request.POST["comment"]
        id1 = request.POST["id"]
        user = request.user
        co = Comment(catalog = Listing.objects.filter(id=id1).first(), user = user, text = text)
        co.save()
        return HttpResponseRedirect(reverse("item", kwargs = {"id1": id1}))


def new_watch(request, id):
    wa = Watchlist(user = request.user, catalog = Listing.objects.get(id = id))
    wa.save()
    return HttpResponseRedirect(reverse("item", kwargs = {"id1": id}))


def del_watch(request, id):
    wa = Watchlist.objects.filter(user =request.user, catalog = Listing.objects.get(id = id)).first()
    wa.delete()
    return HttpResponseRedirect(reverse("item", kwargs = {"id1": id}))


def watchlist(request):
    wa = Watchlist.objects.filter(user = request.user)
    return render(request, "auctions/watchlist.html", {"watchlist": wa})


def categories(request):
    ca = Listing.objects.values("category").distinct()
    return render(request, "auctions/category.html", {"ca": ca})


def cat_item(request, name):
    li = Listing.objects.filter(category = name)
    return render(request, "auctions/categ_item.html", {"ca": li})
