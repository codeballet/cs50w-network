from django.contrib.auth import authenticate, login, logout
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

    # get likes counts
    likes = []

    return render(request, "network/index.html", {
        "message": message,
        "page_obj": page_obj,
    })


def like(request, post_id):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(pk=post_id)
            post.like.add(request.user)
            post.save()
        except:
            return render(request, "network/index.html", {
                "message": "Like not added"
            })

    return HttpResponseRedirect(reverse("index"), {
        "message": "Like added"
    })


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

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile": profile,
        "page_obj": page_obj
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
