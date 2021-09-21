import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Post, User


def index(request):
    message = ''
    if request.method == "POST" and request.user.is_authenticated:
        # attempt to save post to database
        try:
            content = request.POST["content"]

            post = Post.objects.create(
                user=request.user, content=content)
            post.save()

            message = "Post successfully created!"
        except:
            message = "Failed to add post!"

    # set up pagination
    posts = Post.objects.order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # get like counts
    likes = []
    for page in page_obj:
        likes.append(page.like.count())

    return render(request, "network/index.html", {
        "message": message,
        "page_obj": page_obj,
        "likes": likes
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


def profile(request, user_id):
    profile = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=profile).order_by('-timestamp')

    # set up pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # get like counts
    likes = []
    for page in page_obj:
        likes.append(page.like.count())

    return render(request, "network/profile.html", {
        "profile": profile,
        "page_obj": page_obj,
        "likes": likes
    })


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


# API
@login_required
def like(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    # get the body of the request
    data = json.loads(request.body)

    # like or unlike
    try:
        post = Post.objects.get(pk=post_id)
        if post.user == request.user:
            return JsonResponse({"message": "You cannot like your own post"}, status=406)
        elif data['wish'] == 'like':
            post.like.add(request.user)
            post.save()
            return JsonResponse({"message": "Like added"}, status=201)
        elif data['wish'] == 'unlike':
            post.like.remove(request.user)
            post.save()
            return JsonResponse({"message": "Like removed"}, status=201)
    except:
        return JsonResponse({"error": "Like not added"}, status=400)


def likes_count(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        likes = post.like.count()
        return JsonResponse({
            "likes": likes
        }, status=200)
    except:
        return JsonResponse({
            "error": f"Could not acquire likes for post id {post_id}"
        }, status=400)


def likers(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        likers = post.like.all()
        likers_list = []
        for liker in likers:
            likers_list.append(liker.username)

        return JsonResponse({
            "likers": likers_list
        }, status=200)
    except:
        return JsonResponse({
            "error": f"Could not acquire post id {post_id}"
        }, status=400)


@login_required
def follow(request, user_id):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required"
        }, status=400)

    try:
        # acquire the followed and following users
        followed = User.objects.get(pk=user_id)
        follower = User.objects.get(pk=request.user.id)

        # add the followed user to the following user
        follower.following.add(followed)

        return JsonResponse({
            "followed": followed.username,
            "follower": follower.username
        })
    except:
        return JsonResponse({
            "error": f"could not register to follow user id {user_id}"
        }, status=400)
