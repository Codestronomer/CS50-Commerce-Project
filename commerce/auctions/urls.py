from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuctionListingsView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.CreateListing.as_view(), name="create_listing"),
    path("bid/<int:pk>", views.bid_form, name="bid"),
    path("<int:pk>", views.AuctionListingView.as_view(), name="detail"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:pk>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/remove/<int:pk>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("close_listing/<int:pk>", views.close_auction, name="close_auction"),
    path("comment/add/<int:pk>", views.add_comment, name="add_comment"),
    path("category/<int:pk>", views.category_view, name="category")
]
