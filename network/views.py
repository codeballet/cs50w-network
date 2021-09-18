import json
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

    posts = Post.objects.order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "message": message,
        "page_obj": page_obj
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


def create_post(request):
    if request.method == "POST" and request.user.is_authenticated:
        # attempt to save post to database
        try:
            data = json.loads(request.body)
            content = data.get("content", "")

            post = Post.objects.create(
                user=request.user, content=content)
            post.save()

            return JsonResponse({
                "message": "Post added successfully"
            }, status=201)
        except:
            return JsonResponse({
                "error": "Post not added to database"
            }, status=400)


def posts(request):
    posts = Post.objects.order_by('-timestamp')
    return JsonResponse([post.serialize() for post in posts], safe=False)


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


def user_posts(request):
    try:
        data = json.loads(request.body)
        user = data.get("user", "")
        user_posts = Post.objects.filter(user=user).order_by('-timestamp')
        return JsonResponse(
            [post.serialize() for post in user_posts], safe=False
        )
    except:
        return JsonResponse({
            "error": "Cannot acquire posts from user"
        })
