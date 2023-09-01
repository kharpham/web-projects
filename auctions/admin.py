from django.contrib import admin
from .models import User, Category, AuctionListing, Bid, Comment


# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "starting_bid", "current_bid", "active", "winner")
    exclude = ('current_bid',)

admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
