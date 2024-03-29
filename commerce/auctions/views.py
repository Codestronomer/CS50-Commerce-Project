from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import AuctionListingForm, BidForm, WatchListForm, CommentForm

from .models import User, AuctionListing, Comment, Bid, WatchList, Category


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
            WatchList.objects.create(user=user)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required()
def bid_form(request, pk):
    if request.method == "POST":
        auction = AuctionListing.objects.get(pk=pk)
        user = User.objects.get(username=request.user)
        amount = request.POST.get('amount')
        if auction.last_bid:
            if int(amount) < int(auction.last_bid.amount):
                messages.error(request, "Amount is lower than last bid")
            elif int(amount) < int(auction.bid):
                messages.error(request, "Amount is lower than initial bid")
            else:
                bid = Bid.objects.create(user=request.user, auction=auction, amount=amount)
                auction.bids.add(bid)
                auction.last_bid = bid
                auction.save()
            return redirect(reverse("detail", args=[pk]))
        else:
            bid = Bid.objects.create(user=request.user, auction=auction, amount=amount)
            auction.bids.add(bid)
            auction.last_bid = bid
            auction.save()
        return redirect(reverse("detail", args=[pk]))
    else:
        return render(request, "auctions/detail.html", {"bid_form": BidForm()})


class CreateListing(LoginRequiredMixin, FormView):
    form_class = AuctionListingForm
    template_name = "auctions/create_listing.html"
    success_url = '/'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AuctionListingsView(ListView):
    model = AuctionListing
    template_name = "auctions/index.html"
    context_object_name = "listings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = context['listings'].filter(is_closed=False)
        context['categories'] = Category.objects.all()
        return context




class AuctionListingView(DetailView):
    model = AuctionListing
    template_name = "auctions/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context


@login_required()
def close_auction(request, pk):
    if request.method == "GET":
        auction = AuctionListing.objects.get(pk=pk)
        auction.is_closed = True
        auction.save()
    return redirect(reverse("detail", args=[pk]))


@login_required()
def watchlist(request):
    if request.user.is_authenticated:
        my_watchlist = WatchList.objects.get(user=request.user)
        return render(request, "auctions/watchlist.html", {"watchlist": my_watchlist})


@login_required()
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


@login_required()
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


@login_required()
def add_comment(request, pk):
    if request.method == "POST":
        auction = AuctionListing.objects.get(pk=pk)
        comment = request.POST.get('comment')
        user = request.user
        Comment.objects.create(user=user, comment=comment, listing=auction)
        return redirect(reverse("detail", args=[pk]))
    else:
        return render(request, "auctions/detail.html", {"comment_form": CommentForm()})


def category_view(request, pk):
    category_name = Category.objects.get(pk=pk)
    active_listing = AuctionListing.objects.filter(is_closed=False, category=category_name)
    return render(request, 'auctions/category.html', {'listings': active_listing, 'category_name': category_name})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'auctions/category_list.html', {"categories": categories})
