from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"
class AuctionListing(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(_("Starting bid($)"),decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, default=Category.objects.get(category="Others").id, blank=True, related_name="listings")
    created_at = models.DateTimeField(_("Create at"),auto_now_add=True)
    image_url = models.URLField(_("Image URL(Optional)"),max_length=200, blank=True)
    active = models.BooleanField(default=True)
    current_bid = models.DecimalField(_("Current bid(Optional)"),decimal_places=2, max_digits=10, default=None, blank=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.image_url:
            self.image_url = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930"
        if not self.current_bid:
            self.current_bid = self.starting_bid
        super(AuctionListing, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title.capitalize()} (Created {self.creater.username.capitalize()}, {self.created_at.strftime('%B %d, %Y, %I:%M %p')})"
# Create a Bid model including the bid maker, the listing that the bid is placed on, the price of the bid and the timestamp
class Bid(models.Model):
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(_("Place bid (At least as large as the current bid):"), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_("Create at"),auto_now_add=True)
    def __str__(self):
        return f"{self.maker.username.capitalize()} has placed a bid of {self.price}$ ({self.created_at.strftime('%B %d, %Y, %I:%M %p')})"

# Create a Comment model including the comment maker, the listing that the comment is on, the content of the comment and the timestamp
class Comment(models.Model):
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(_("Create at"),auto_now_add=True)
    def __str__(self):
        return f"{self.maker.username.capitalize()}, (created at {self.created_at.strftime('%B %d, %Y, %I:%M %p')})"