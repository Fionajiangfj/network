from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import *


def index(request):
    if request.method == 'GET':
        all_posts = Post.objects.all().order_by('timestamp').reverse()
        paginator = Paginator(all_posts, 2)  #devide all posts in 10
        
        page_number = request.GET.get("page")
        page_posts = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            'posts': all_posts,
            'page_posts': page_posts
        })
    else:
        return HttpResponseNotAllowed(['GET'])


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


def new_post(request):
    if request.method == 'POST':
        content = request.POST.get('new_post')
        if not content:
            messages.error(request, "Content area can not be blank.")
            return HttpResponseRedirect(reverse('index'))
        
        #store the new post
        Post.objects.create(
            username=request.user,
            content=content
            )
        
        #redirect to index page
        return HttpResponseRedirect(reverse('index'))
    
    
def profile(request, username):
    profile_user = User.objects.get(username=username)
    posts = profile_user.posts.all().order_by('timestamp').reverse()
    user = request.user
    #if profile_user
    if request.user == profile_user:
        is_user = True
    else:
        is_user = False
        
    #if followers
    followers =  profile_user.followers.all().count()
    
    #if following list is not empty
    if profile_user.following is not None:
        following_num = profile_user.following.all().count()
    else:
        following_num = 0
        
    #if user has followed the profile_user
    if user.following is not None:
        if profile_user in user.following.all():
            has_follow = True
        else:
            has_follow = False
    else:
        has_follow = False
        
    return render(request, 'network/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'followers': followers,
        'following_num': following_num,
        'has_follow': has_follow,
        'is_user': is_user
    })
    
    
def follow_or_unfollow(request, profile_user_id):
    profile_user = User.objects.get(pk=profile_user_id)
    user = request.user
    action = request.POST.get('action')
    
    if action == 'follow':
        # add profile_user to user's following list
        user.following.add(profile_user)
        
    else:
        # remove profile_user from user's following list
        user.following.remove(profile_user)
        
    # save user
    user.save()
        
    return HttpResponseRedirect(reverse('profile', args=[profile_user.username]))


def following(request):
    #get the following list
    following_list = request.user.following.all()
    
    #get the posts made by the following list
    following_posts = Post.objects.filter(username__in=following_list).order_by('timestamp').reverse()
    
    return render(request, 'network/following.html', {
        'following_posts': following_posts
    })
    

def edit(request, post_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            
            # Load the JSON data from request body
            data = json.loads(request.body.decode('utf-8'))  # <-- Added this line to read JSON payload
            edited_content = data.get('content', None)  # <-- Get the edited content from JSON data
            
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Post not found or you don't have permission to edit it."}, status=404)
            
            # Update the post content
            post.content = edited_content
            post.save()
            
            # Return a JSON response with the updated content
            return JsonResponse({"updatedContent": post.content})
        
        else:
            return JsonResponse({"error": "Authentication required to edit posts."}, status=401)
    
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
            

def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    
    if request.method == 'POST':
        liked = Like.objects.filter(username=user, post=post)
        
        if liked.exists():
            liked.delete()
            status = 'unliked'
            
        else:
            Like.objects.create(username=user, post=post)
            status = 'liked'
            
        return JsonResponse({"status": status})