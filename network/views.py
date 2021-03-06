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


@login_required
def following(request):
    following = request.user.following.all()
    print(following)

    posts = Post.objects.order_by('-timestamp').filter(user__in=following)
    print(posts)

    # set up pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # get like counts
    likes = []
    for page in page_obj:
        likes.append(page.like.count())

    return render(request, "network/following.html", {
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


#######
# API #
#######

@login_required
def like_api(request, post_id):
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


def likes_count_api(request, post_id):
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


def likers_api(request, post_id):
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
def follow_api(request, user_id):
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
            "message": f"{follower.username} is following {followed.username}"
        }, status=201)
    except:
        return JsonResponse({
            "error": f"could not register to follow user id {user_id}"
        }, status=400)


def followed_api(request, user_id):
    # check if the current user is following the user_id
    try:
        profile = User.objects.get(pk=user_id)

        if profile in request.user.following.all():
            return JsonResponse({
                "following": True
            })
        else:
            return JsonResponse({
                "following": False
            })
    except:
        return JsonResponse({
            "error": "Could not determine if user is following profile"
        })


def followers_api(request, user_id):
    try:
        profile = User.objects.get(pk=user_id)
        users = User.objects.all()
        count = 0

        for user in users:
            if profile in user.following.all():
                count += 1

        return JsonResponse({
            "count": count
        })
    except:
        return JsonResponse({
            "error": "Cannot acquire the followers count"
        })


def following_api(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({
            "count": user.following.count()
        }, status=200)
    except:
        return JsonResponse({
            "error": "Cannot acquire the following count"
        }, status=400)


@login_required
def unfollow_api(request, user_id):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required"
        }, status=400)

    try:
        # acquire the followed and following users
        followed = User.objects.get(pk=user_id)
        follower = User.objects.get(pk=request.user.id)

        # add the followed user to the following user
        follower.following.remove(followed)

        return JsonResponse({
            "message": f"{follower.username} has stopped following {followed.username}"
        }, status=201)
    except:
        return JsonResponse({
            "error": f"could not register to unfollow user id {user_id}"
        }, status=400)


@login_required
def update_api(request, user_id, post_id):
    if request.method != "PUT":
        return JsonResponse({
            "error": "PUT request required"
        }, status=400)

    if user_id != request.user.id:
        return JsonResponse({
            "error": "You are not authorized to edit the post"
        }, status=401)

    try:
        # get the data from the request
        data = json.loads(request.body)
        content = data['content']

        # update the db
        post = Post.objects.get(pk=post_id)
        post.content = content
        post.save()

        # get the new content from db
        updated_post = Post.objects.get(pk=post_id)
        updated_content = updated_post.content

        return JsonResponse({
            "content": updated_content
        }, status=200)

    except:
        return JsonResponse({
            "error": "Could not update post content"
        }, status=400)
