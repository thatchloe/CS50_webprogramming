from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    

class Listing(models.Model):
    title = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    link = models.URLField(max_length=200, blank=True, null=True, default=None)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'"{self.title}"'



class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    bid_listingid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listingid", null=True)
    bid = models.IntegerField()
    

class Comment(models.Model):
    user = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)
    comment_listingid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listingid", null=True)

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True) 
    watchlist_listingid = models.IntegerField(null=True)
    
    def __str__(self):
        return f'{self.watchlist_listingid} Watchlist ID# {self.id} : {self.user} watchlisted : {self.watchlist_listingid}'
    

class Closedbid(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    closedbid_listingid = models.IntegerField()
    winprice = models.IntegerField()
    

class Alllisting(models.Model):
    Alllisting_listingid = models.IntegerField() 
    title = models.CharField(max_length=64)
    description = models.TextField()
    link = models.CharField(max_length=64,default=None,blank=True,null=True)


