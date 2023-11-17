from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

# Import Django Paginator
from django.core.paginator import Paginator
from .models import User, Post



def index(request):
    posts = Post.objects.all().order_by('-timestamp')

    # Create Paginator
    pagination = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = pagination.get_page(page)

    if request.method == "POST":
        content = request.POST["content"]
        # Check if users have provided content to posts
        if content != "":
            new_post = Post.objects.create(creator=request.user, content=request.POST["content"])
            new_post.save()
            new_posts = Post.objects.all().order_by('-timestamp')

            # Create Paginator
            new_pagination = Paginator(new_posts, 10)
            page = request.GET.get('page')
            posts_page = new_pagination.get_page(page)
            return render(request, "network/index.html", {
                "posts": new_posts,
                "alert": f"You have successfully created a new post on {new_post.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
                "posts_page": posts_page,
                "alert_type": "success",
            })
        else:
            return render(request, "network/index.html", {
                "alert": "You haven't provided the content yet!",
                "posts": posts,
                "posts_page": posts_page,
                "alert_type": "unsuccess",
            })
    return render(request, "network/index.html", {
        "posts": posts,
        "posts_page": posts_page,
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

@login_required
def profile(request, username):
    try:
        profile = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(f"Username: {username} doesn't exist")
    if request.method == "POST":
        # Check if one user is trying to follow that user
        if profile == request.user:
            raise Http404(f"Can not follow yourself")
        # Check if user has followed this profile
        elif profile.followers.filter(pk=request.user.pk).exists():
            profile.followers.remove(request.user)
            profile.save()
        elif not profile.followers.filter(pk=request.user.pk).exists():
            profile.followers.add(request.user)
            profile.save()
    posts = Post.objects.filter(creator=profile).order_by("-timestamp")
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = p.get_page(page)
    return render(request, 'network/profile.html', {
        "profile": profile,
        "posts_page": posts_page, 
        "user": request.user,
        "follower_exists": profile.followers.filter(pk=request.user.pk).exists,
        "followers": profile.followers.all().count(),
        "followings": profile.followings.all().count(),
    })
@login_required
def following(request):
    followings = request.user.followings.all()
    posts = Post.objects.filter(creator__in=followings).order_by('-timestamp')

    # Set up Pagination
    pagination = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = pagination.get_page(page)

    return render(request, "network/followings.html", {
        "posts": posts,  
        "posts_page": posts_page,
        })

@login_required
def posts_api(request, profile):
    """Create APIs to store posts for each user"""
    if request.user.username != profile:
        return HttpResponse("One user can only access that user's posts")
    else:
        posts = Post.objects.filter(creator=request.user).order_by('-timestamp')
        return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt
@login_required
def post(request, id):
    """Create APIs to store specific post"""
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({
            "error" : "Post doens't exist"
            }, status = 400)
    if post.creator != request.user:
        return JsonResponse({
            "error": "You can not access to other users' posts APIs",
        }, status = 400)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not "":
            post.content = data["content"]
        else:
            JsonResponse("Content can not be empty")
        post.save()
        return HttpResponse(status=204)
        # return HttpResponse("1")
    elif request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)

# Handle user click Like to a specific post
@csrf_exempt
@login_required
def interact_post(request, id):
    # Get the post object
    try: 
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({
            "error" : "Post doens't exist"
            }, status=400)
    if request.method == "PUT":
        data = json.loads(request.body)
        likes = data.get("likes")
        # The user hit likes
        if request.user.username in likes:
            try:
                post.likes.add(request.user)
            except IntegrityError:
                return JsonResponse({
                    "error": f"The user already likes the post {id}"
                }, status=400)
            post.save()
            return HttpResponse(status=204)
        # The user hit unlikes
        elif request.user.username not in likes:
            try:
                post.likes.remove(request.user)
            except ValueError:
                return JsonResponse({
                    "error": f"The user already doesn't like the post {id}"
                }, status=400)
            post.save()
            return HttpResponse(status=204)
    elif request.method == "GET":
        return JsonResponse(post.serialize_like_post(), safe=False)