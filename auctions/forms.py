from django import forms
from decimal import Decimal
# listing form for creating a new listing

class ListingForm(forms.Form):
    title = forms.CharField(label='Title', max_length=64)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    starting_bid = forms.DecimalField(label='Starting Bid', decimal_places=2, max_digits=10)
    image_url = forms.URLField(label='Image URL', required=False)
    category = forms.ChoiceField(label='Category', 
                                 choices=[('Fashion', 'Fashion'),
                                          ('Electronics', 'Electronics'), 
                                          ('Home', 'Home'), 
                                          ('Toys', 'Toys'),
                                          ('Health and Beauty', 'Health and Beauty'),
                                          ('Sports and Outdoors', 'Sports and Outdoors'),
                                          ('Automotive', 'Automotive'),
                                          ('Books', 'Books'),
                                          ('Movies and Music', 'Movies and Music'),
                                          ('Collectibles', 'Collectibles'),
                                          ('Art', 'Art'),
                                          ('Other', 'Other')])
    
class BidForm(forms.Form):
    bid = forms.DecimalField(label="Bid amount", max_digits=10, decimal_places=2)
    
class CommentForm(forms.Form):
    content = forms.CharField(label='Comment', widget=forms.Textarea)