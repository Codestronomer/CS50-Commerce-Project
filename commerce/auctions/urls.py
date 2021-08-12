from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuctionListingsView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.CreateListing.as_view(), name="create_listing"),
    path("<str:name>", views.AuctionListingView.as_view(), name="detail"),
]
