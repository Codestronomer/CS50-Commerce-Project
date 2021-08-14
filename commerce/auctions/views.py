from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, ListView, DetailView
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages import SUCCESS
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AuctionListingForm, BidForm, WatchListForm

from .models import User, AuctionListing, Comment, Bid, WatchList


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


def bid_form(request, pk):
    if request.method == "POST":
        auction = AuctionListing.objects.get(pk=pk)
        user = User.objects.get(username=request.user)





class CreateListing(FormView):
    form_class = AuctionListingForm
    template_name = "auctions/create_listing.html"
    success_url = '/'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)


class AuctionListingsView(ListView):
    model = AuctionListing
    template_name = "auctions/index.html"
    context_object_name = "listings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = context['listings'].filter(is_closed=False)
        return context


class AuctionListingView(DetailView):
    model = AuctionListing
    template_name = "auctions/detail.html"


def watchlist(request):
    if request.user.is_authenticated:
        my_watchlist = WatchList.objects.get(user=request.user)
        return render(request, "auctions/watchlist.html", {"watchlist": my_watchlist})


def add_to_watchlist(request, pk):
    if request.method == "POST":
        coming_auction = AuctionListing.objects.get(pk=pk)
        watchlist = WatchList.objects.get(user=request.user)
        if coming_auction in watchlist.auctions.all():
            watchlist.auctions.remove(coming_auction)
            watchlist.save()
        else:
            watchlist.auctions.add(coming_auction)
            watchlist.save()
        return redirect("/")
    else:
        return render(request, "auctions/detail.html", {'watchlist_form': WatchListForm()})


def remove_from_watchlist(request, pk):
    if request.method == "POST":
        watchlist = WatchList.objects.get(user=request.user)
        deleted_auction = AuctionListing.objects.get(pk=pk)
        if deleted_auction in watchlist.auctions.all():
            watchlist.auctions.remove(deleted_auction)
            watchlist.save()
            return redirect("watchlist")
    else:
        return render(request, "auctions/watchlist.html", {'watchlist_form': WatchListForm()})
