from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from .models import User, AuctionListing, Bid, Comment, Category
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist


# Create new listing form
class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'category', 'image_url']
        # Not include creater, current_bid, active, watchers and created_at fields
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs ={'class': 'form-control'}),
            "starting_bid": forms.NumberInput(attrs={"class": 'form-control','min': '0.01'}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "autocomplete": "off"}),
        }

# Create comment form:
class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Add a comment")


def index(request):
    listings = AuctionListing.objects.filter(active=True).order_by('-created_at')
    return render(request, "auctions/index.html", {
        "listings": listings,
        "option": "active",
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

# Return page of closed listings
def closed_listing(request):
    listings = AuctionListing.objects.filter(active=False).order_by('-created_at')
    return render(request, "auctions/index.html", {
        "listings": listings,
        "option": "closed",
    })
# Return page of all listings incuding both closed and active listings
def all_listing(request):
    listings = AuctionListing.objects.all().order_by('-created_at')
    return render(request, "auctions/index.html", {
        "listings": listings,
        "option": "all",
    })
# Create new listing
@login_required
def create(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.current_bid = form.starting_bid
            form.creater = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form,
            })
    return render(request, "auctions/create.html",{
        "form": AuctionListingForm(),
    })

@login_required
def view_listing(request, listing_id):
    form = CommentForm()
    listing = AuctionListing.objects.get(id=listing_id)
    # Close the bidding by the listing creator
    if request.method == "POST":
        listing.active = False
        if listing.bids.all().count() != 0:
            listing.winner = listing.bids.get(price=listing.current_bid).maker
        listing.save()
        return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))

    try:
        bid_owner = listing.bids.get(price=listing.current_bid).maker
    except ObjectDoesNotExist:
        bid_owner = None
    if listing:
        return render(request,"auctions/view_listing.html", {
            "listing": listing,
            "in_watchlist": request.user in listing.watchers.all(),
            "is_creator": listing.creater == request.user,
            "bids_count": listing.bids.all().count(),
            "bids": listing.bids.all().order_by('-created_at'),
            "bid_owner": bid_owner,
            "form": form,
            "comments": listing.comments.all().order_by('-created_at'),
        })
    else:
        return Http404("Oops... Page not found!")

@login_required
def watchlist_view(request):
    watchlist = request.user.watchlist.all().order_by('-created_at')
    print(watchlist)
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist,
    })

# Add listing to user's watchlist
@login_required
def add_to_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchers.add(request.user)
    return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))

# Remove listing from user's watchlist
@login_required
def remove_from_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchers.remove(request.user)
    return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))

# Let the user place bids on item
@login_required
def place_bid(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    # Form for placing bids
    class BidForm(forms.Form):
        bid = forms.FloatField(min_value=listing.current_bid, label="Enter bid")
    # POST method case
    if request.method == "POST":
        bids_count = listing.bids.all().count()
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            # In case there are no bids yet, bids_count >= listing.current_bid.
            # In case there are already bids, bids_count >=  listing.current_bid
            if bids_count == 0 or (bids_count != 0 and bid > listing.current_bid):
                new_bid = Bid.objects.create(maker=request.user, listing=listing, price=bid)
                new_bid.save()
                listing.current_bid = bid
                listing.save()
                return HttpResponseRedirect(reverse("view_listing", args=[listing.id]))
            # In case there are bids already, bids_count == listing.current_bid => Not valid
            else:
                return render(request, "auctions/place_bid.html", {
                    "listing": listing,
                    "form": form,
                    "bids_count": bids_count,
                    "message": "Your bid must be greater than the current bid",
                })
    # GET method case
    if listing.creater != request.user and listing.active == True:
        return render(request, "auctions/place_bid.html", {
            "listing": listing,
            "bids_count": listing.bids.all().count(),
            "form": BidForm(),
        })
    elif listing.creater == request.user:
        # Render errors to the user
        return render(request, "auctions/view_listing.html", {
            "listing": listing,
            "bids": listing.bids.all().order_by('-created_at'),
            "message": "The listing creator can not place bid",
        })
    else:
        return HttpResponse("The listing has been closed")
    
@login_required
def add_comment(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except ObjectDoesNotExist:
        return HttpResponse("Listing does not exist")
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(maker=request.user, listing=listing, content = form.cleaned_data['comment'])
            comment.save()
        return HttpResponseRedirect(reverse("view_listing", args=[listing.id]))

def categories(request):
    categories = Category.objects.all().order_by('-id')
    return render(request, "auctions/categories.html", {
        'categories': categories,
    })

def categories_listing(request, category):
    category_object = Category.objects.get(category=category)
    listings = AuctionListing.objects.filter(category=category_object, active=True)
    return render(request, "auctions/index.html", {
        'listings': listings,
        'option': 'category',
        'category': category_object,
    })



