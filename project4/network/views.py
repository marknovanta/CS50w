import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post, Follow, Like


def index(request):
    header = "All Posts"
    if request.method == "GET":
        
        likes = Like.objects.all()
        posts = Post.objects.all().order_by("-id")
        
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        liked_post = list()
        try:
            for like in likes:
                if request.user.id == like.user.id:
                    liked_post.append(like.post.id)
        except:
            liked_post = []

        return render(request, "network/index.html", {
            "posts": page_obj, "comments": True, "header": header, "likes": liked_post})
    else:
        likes = Like.objects.all()
        liked_post = list()
        try:
            for like in likes:
                if request.user.id == like.user.id:
                    liked_post.append(like.post.id)
        except:
            liked_post = []

        now = datetime.now().strftime("%b %d %Y, %H:%M %p")
        #print(now.strftime("%b %-d %Y, %-H:%M %p"))
        post = Post(user=request.user, timestamp=now, content=request.POST.get('content'))
        post.save()

        posts = Post.objects.all().order_by("-id")
        paginator = Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "posts": page_obj, "comments": True, "header": header, "likes": liked_post})


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

def profile_render(request, user):

    likes = Like.objects.all()
    liked_post = list()
    try:
        for like in likes:
            if request.user.id == like.user.id:
                liked_post.append(like.post.id)
    except:
        liked_post = []

    u = User.objects.filter(id=user)
    
    followers = len(Follow.objects.all().filter(follows=u[0]))
    following_usr = len(Follow.objects.all().filter(follower=u[0]))
    
    visitor = User.objects.filter(id=request.user.id)
    posts = Post.objects.filter(user=user).order_by("-id")
    v_followings = Follow.objects.all().filter(follower=visitor[0])

    v_followings_list = list()
    for f in v_followings:
        v_followings_list.append(f.follows.username)
    following = str(u[0]) in v_followings_list
    print(v_followings_list)
    print(following)

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return {"posts": page_obj,
        "visitor": visitor[0],
        "u": u[0], 
        "following": following, 
        "followers": followers,
        "following_usr": following_usr,
        "likes": liked_post
    }


def user_page(request, user):
    if request.method == "GET":
        return render(request, "network/user_page.html", profile_render(request, user))
    else:
        u = User.objects.filter(id=user)
        visitor = User.objects.filter(id=request.user.id)
        action = request.POST.get("action")
        if action == "follow":
            f = Follow.objects.create(follower=request.user, follows=u[0])
            f.save()
            print("FOLLOWING")
        else:
            f = Follow.objects.filter(follower=request.user, follows=u[0])
            print(f)
            f.delete()
            print('UNFOLLOW')
        return render(request, "network/user_page.html", profile_render(request, user))

@login_required(login_url='login')
def following(request):
    header = "Following Posts"
    if request.method == "GET":

        likes = Like.objects.all()
        liked_post = list()
        try:
            for like in likes:
                if request.user.id == like.user.id:
                    liked_post.append(like.post.id)
        except:
            liked_post = []

        followed_usrs = Follow.objects.all().filter(follower=request.user.id)

        followed_list = list()
        for u in followed_usrs:
            followed_list.append(u.follows.id)
       
        posts = Post.objects.all().filter(user__in=followed_list).order_by("-id")

        paginator = Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {"posts": page_obj, "comments": False, "header": header, "likes": liked_post})
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def post_edit(request, post_id):

    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if post.user != request.user:
        return JsonResponse({"error": "User not authorized to edit"})

    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
def like_dislike(request, post_id):
    post = Post.objects.get(pk=post_id)

    data = json.loads(request.body)
    if data.get("action") == 'like':
        like = Like(user=request.user, post=post)
        like.save()
    else:
        dislike = Like.objects.filter(user=request.user, post=post)
        dislike.delete()
    
    # count new likes
    count = Like.objects.all().filter(post=post)
    post.likes = len(count)
    post.save()

    return HttpResponse(status=204)