from django.contrib import admin
from .models import AuctionListing, Comment, Bid, User, WatchList

# Register your models here.
admin.site.register(AuctionListing)


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'description', 'category', 'image_url', 'created', 'watchlist', 'bid', 'is_closed')
    list_filter = ('is_closed', 'created', 'updated', 'category')
    search_fields = ('name', 'owner', 'category', 'description')


admin.site.register(Comment)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_on', 'active', 'listing')
    list_filter = ('active', 'created_on', 'updated_on', 'listing')
    search_fields = ('user', 'comment', 'listing')


admin.site.register(User)


admin.site.register(Bid)


class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')
    list_filter = ('user',)


admin.site.register(WatchList)

