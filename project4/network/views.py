from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, UserFollowing
from django.contrib.auth.decorators import login_required, csrf_exempt
from django.core.paginator import Paginator

def index(request):
    try:
        posts = Post.objects.all().order_by('-time')
    except:
        posts = None
    return render(request, "network/index.html", {"posts": posts})


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
    
    
@login_required('index')
def post_submit(request):
    if request.method == "POST":
        content = request.POST['content']
        post = Post.objects.create(user_id=request.user.id, user=request.user.username, content=content, likes=0)
        post.save()
        return render(request, "network/index.html")
    else:
        return redirect("index")

def all_posts(request):
    posts = Post.objects.all().order_by('-time')
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, "network/allposts.html", {
            "posts": posts
            })      

@login_required()
def profile(request, profile_id):
    try:
        user = User.objects.get(id=request.user.id)
        profile = User.objects.get(id=profile_id)
        try:
            following = profile.following.all()
            followers = profile.followers.all()
            if user in followers:
                followed = True
            else:
                followed = False
        except:
            following = None
            followers = None
            followed = False
        posts = Post.objects.filter(user_id=profile_id).order_by('-time') 
        paginator = Paginator(posts, 10)
        
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
        
        
        return render(request, 'network/profile.html', {
            'user': user,
            'posts': posts,
            'following': following,
            'followers': followers,
            'followed': followed
            })
        
    except:
        return render(request, "network/profile.html", {
            "error": True
            })
    
@login_required
def follow(request):
    if request.method == 'POST':
        follow_id = request.POST.get('follow_id')
        following = UserFollowing.objects.create(user_id=follow_id, following_user_id=request.user.id)
        following.save()
    
   
    return redirect("profile", profile_id=follow_id)



@login_required
def unfollow(request):
    if request.method == 'POST':
        unfollow_id = request.POST.get('unfollow_id')
        following = UserFollowing.objects.filter(user_id=unfollow_id, follow_user_id=request.user.id)
        following.remove()
    
    
    return redirect("profile", profile_id=unfollow_id)
    
  
@login_required  
def following(request):
    user = User.objects.get(id=request.user.id)
    following = user.following.all()
    posts = Post.objects.filter(user_id=following).order_by('-time')
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, "network/allposts.html", {
            "posts": posts
            }) 
        
@login_required
def like(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        user = User.objects.get(id=request.user.id)
        try:
            post = Post.objects.filter(id=post_id)
        except:
            return redirect("index")
    if user in post.like:
        post.like.remove(user)
    else:
        post.like.add(user)



@login_required
@csrf_exempt
def edit(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        new_post = request.POST.get('post')
        try:
            post = Post.objects.get(id=post_id)
            if post.user == request.user:
                post.content = new_post.strip()
                post.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)
    
    return JsonResponse({}, status=400)
        
    
    
    

    