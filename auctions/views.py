from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm
from .models import User



def index(request):
    listings = Listing.objects.filter(active=True)
    context = {'listings': listings}
    return render(request, 'auctions/index.html', context)


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
    
@login_required    
def newListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd["title"]
            description = cd["description"]
            starting_bid = float(cd["starting_bid"])
            image_url = cd["image_url"]
            category = cd["category"]
            user = request.user
            listing = Listing(title=title, description=description, starting_bid=starting_bid, current_bid=starting_bid, image_url=image_url, category=category, user=user)
            listing.save()
            
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
        return render(request, "auctions/newListing.html", {'form': form})
    
def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing does not exist")
    form = BidForm()
    form2 = CommentForm()
    comments = Comment.objects.filter(listing=listing)
    return render(request, 'auctions/listing.html', {'listing': listing, 'form': form, 'form2': form2, 'comments': comments,})

@login_required
def add_wishlist(request, listing_id):
    user = request.user
    listing = get_object_or_404(Listing, pk=listing_id)

    user.wishlist.add(listing)
    messages.success(request, f"Added {listing.title} to wishlist.")

    return redirect("listing", listing_id=listing_id)

@login_required
def remove_wishlist(request, listing_id):
    user = request.user
    listing = get_object_or_404(Listing, pk=listing_id)

    user.wishlist.remove(listing)
    messages.success(request, f"Removed {listing.title} from wishlist.")

    return redirect("listing", listing_id=listing_id)

@login_required
def bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    form = BidForm(request.POST)
    form2 = CommentForm()
    comments = Comment.objects.filter(listing=listing)
    if form.is_valid():
        bid_amount = form.cleaned_data["bid"]
        if bid_amount > listing.current_bid or (listing.current_bid == listing.starting_bid and bid_amount == listing.starting_bid):
            listing.current_bid = bid_amount
            listing.winner = request.user
            listing.save()
            message1 = f"Your bid of ${bid_amount} has been placed."
            return render(request, 'auctions/listing.html', {'listing': listing, 'form': form, 'form2' : form2, 'message1': message1, 'comments': comments})        
        else:
            message2 = f"Your bid must be higher than the current bid of ${listing.current_bid}."
            return render(request, 'auctions/listing.html', {'listing': listing, 'form': form, 'form2' : form2, 'message2': message2, 'comments': comments})    
    else:
        return render(request, 'auctions/listing.html', {'listing': listing, 'form': form, 'form2' : form2, 'comments': comments})

@login_required    
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing.active = False
    listing.save()
    return redirect("listing", listing_id=listing_id)

@login_required
def comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        comment = cd["content"]
        user = request.user
        comment = Comment(content=comment, user=user, listing=listing)
        comment.save()
        return redirect("listing", listing_id=listing_id)    
    else:
        return redirect("listing", listing_id=listing_id)

@login_required    
def wishlist(request):
    user = request.user
    listings = user.wishlist.all()
    return render(request, 'auctions/wishlist.html', {'listings': listings})

def categories(request):
    return render(request, 'auctions/categories.html')

def category_listing(request, category):
    listings = Listing.objects.filter(category=category, active=True)
    return render(request, 'auctions/category_listing.html', {'listings': listings, 'category': category})