from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    wishlist = models.ManyToManyField('Listing', blank=True, null=True, related_name="wishlisted")
    def __str__(self):
        return f"{self.username}"
    
# class Listing(models.Model):

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    current_bid = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listings", blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"
    
class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.user.username} bid {self.bid}$ on {self.listing.title}"
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return f"{self.user.username} commented on {self.listing.title} on {self.date}"
    