from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from .models import User, Listing, Bid, Comment, Watchlist, Closedbid, Alllisting
from django.contrib.auth.decorators import login_required

def index(request):
    items = Listing.objects.all()
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request, "auctions/index.html", { 'items' : items,
                                                   'wcount': wcount
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

@login_required(redirect_field_name='index')
def create(request):
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/create.html",{
        "wcount":wcount
    })
        

@login_required(redirect_field_name='index')
def createsubmit(request):
    if request.method == "POST":
        listing = Listing()
        listing.owner = request.user.username
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.price = request.POST.get('startingBid')
        listing.category = request.POST.get('category')
        if request.POST.get('link'):
            listing.link = request.POST.get('link')
        else:
            listing.link = "https://wallpaperaccess.com/full/1605486.jpg"
        listing.save()
        All = Alllisting()
        items = Listing.objects.all()
        for i in items:
            try:
                if Alllisting.objects.get(Alllisting_listingid=i.id):
                    pass
            except:
                All.Alllisting_listingid = i.id
                All.title = i.title
                All.description = i.description
                All.link = i.link
                All.save()
        return redirect('index')
    else:
        return redirect('index')
        
    
def listing(request, listingid):
    try:
        item = Listing.objects.get(id=listingid)
    except:
        return redirect("index")
    try:
        comments = Comment.objects.filter(comment_listingid=listingid)
    except:
        comments = None
    if request.user.username:
        try:
            if Watchlist.objects.get(user=request.user.username,watchlist_listingid=listingid):
                added=True
        except:
            added = False
        try:
            l = Listing.objects.get(id=listingid)
            if l.owner == request.user.username :
                owner=True
            else:
                owner=False
        except:
            return redirect('index')
    else:
        added=False
        owner=False
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/listing.html",{
        "i":item,
        "error":request.COOKIES.get('error'),
        "errorgreen":request.COOKIES.get('errorgreen'),
        "comments":comments,
        "added":added,
        "owner":owner,
        "wcount": wcount
    })
            



@login_required(redirect_field_name='index')
def addwatchlist(request, listingid):
    w = Watchlist()
    w.user = request.user.username
    w.watchlist_listingid = listingid
    w.listing = Listing.objects.get(id=listingid)
    w.save()
    return redirect('listing',listingid=listingid)
   





@login_required(redirect_field_name='index')
def removewatchlist(request, listingid):
    try:
        w = Watchlist.objects.get(user=request.user.username,watchlist_listingid=listingid, listing=Listing.objects.get(id=listingid))
        w.delete()
        return redirect('listing',listingid=listingid)
    except:
        return redirect('listing',listingid=listingid)
        



@login_required(redirect_field_name='index')
def watchlist(request,username):
    try:
        w = Watchlist.objects.filter(user=username)
        items = []
        for i in w:
            items.append(Listing.objects.filter(id=i.watchlist_listingid))
        try:
            w = Watchlist.objects.filter(user=request.user.username)
            wcount=len(w)
        except:
            wcount=None
        return render(request,"auctions/watchlist.html",{
            "items":items,
            "wcount":wcount
        })
    except:
        try:
            w = Watchlist.objects.filter(user=request.user.username)
            wcount=len(w)
        except:
            wcount=None
        return render(request,"auctions/watchlist.html",{
            "items":None,
            "wcount":wcount
        })
    




@login_required(redirect_field_name='index')
def bidsubmit(request, listingid):
    listing = Listing.objects.get(id=listingid)
    current_bid = listing.price
    if request.method == "POST":
            user_bid = int(request.POST.get("bid"))
            if user_bid > current_bid:
                listing.price = user_bid
                listing.save()
                try:
                    if Bid.objects.filter(bid_listingid=listingid):
                        bidrow = Bid.objects.filter(bid_listingid=listingid)
                        bidrow.delete()
                    bid = Bid()
                    bid.user = request.user.username
                    bid.title = listing.title
                    bid.bid_listingid = listingid
                    bid.listing = listing
                    bid.bid = user_bid
                    bid.save()
                
                except:
                    bid = Bid()
                    bid.user = request.user.username
                    bid.title = listing.title
                    bid.bid_listingid = listingid
                    bid.listing = listing
                    bid.bid = user_bid
                    bid.save()
                    
                response = redirect('listing',listingid=listingid)
                response.set_cookie('errorgreen','bid successful!!!',max_age=3)
                return response
            else:
                response = redirect('listing',listingid=listingid)
                response.set_cookie('error','Bid should be greater than current price',max_age=3)
                return response
       
    else:
        return redirect('index')




@login_required(redirect_field_name='index')                   
def closebid(request, listingid):
    try:
        listing = Listing.objects.get(id=listingid)
    except:
        return redirect('index')
    closedbid = Closedbid()
    title = listing.title
    closedbid.owner = listing.owner
    closedbid.closedbid_listingid = listingid
    try:
        bidrow = Bid.objects.get(bid_listingid=listingid, bid=listing.price)           
        closedbid.winner = bidrow.user
        closedbid.winprice = bidrow.bid
        closedbid.save()
        bidrow.delete()
    except:
        closedbid.winner = listing.owner
        closedbid.winprice = listing.price
        closedbid.save()
    
    try:
        cblist = Closedbid.objects.get(closedbid_listingid=listingid)
    except:
        closedbid.owner = listing.owner
        closedbid.winner = listing.owner
        closedbid.closedbid_listingid = listingid
        closedbid.winprice = listing.price
        closedbid.save()
        cblist = Closedbid.objects.get(closedbid_listingid=listingid)
    listing.delete()
    
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/winningpage.html",{
        "cb":cblist,
        "title":title,
        "wcount":wcount
    })   

      

        

@login_required(redirect_field_name='index')
def winnings(request):
    items = []
    try:
        wonitems = Closedbid.objects.filter(winner=request.user.username)
        for i in wonitems:
            items.append(Alllisting.objects.filter(Alllisting_listingid=i.closedbid_listingid))
    except:
        wonitems = None
        items = None
    
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount = len(w)
    except:
        wcount = None
    
    return render(request, 'auctions/winnings.html',{
        "items": items,
        "wcount": wcount,
        "wonitems": wonitems
            })
    
                
            
            
@login_required(redirect_field_name='index')
def cmntsubmit(request, listingid):
    try:
        listing = Listing.objects.get(id=listingid)
    except:
        return redirect('index')
    if request.method == 'POST':
        comnt = request.POST.get('comment')
        comment = Comment()
        comment.user = request.user.username
        comment.comment = comnt
        comment.comment_listingid = listing.id
        comment.listing = listing
        comment.save()
        return redirect('listing',listingid=listingid)
    else:
        return redirect('index')
    
            

def categories(request):
    items=Listing.objects.raw("SELECT * FROM auctions_listing GROUP BY category")
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/categories.html",{
        "items": items,
        "wcount":wcount
    })


def category(request,category):
    catitems = Listing.objects.filter(category=category)
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/category.html",{
        "items":catitems,
        "category":category,
        "wcount":wcount
    })
    


    
        
        