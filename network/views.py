import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Like, User, Post
from .forms import NewPostForm


def index(request, message: str = None):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # Show 10 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/index.html",
        {
            "like_count": 0,
            "post_form": NewPostForm(),
            "message": message,
            "page_obj": page_obj,
        },
    )


@login_required(login_url="network/login.html")
def following(request, message: str = None):
    posts = Post.objects.filter(creator__in=request.user.following.all())
    paginator = Paginator(posts, 10)  # Show 10 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/index.html",
        {
            "page_obj": page_obj,
            "like_count": 0,
            "post_form": NewPostForm(),
            "message": message,
        },
    )


@login_required(login_url="network/login.html")
def create_post_view(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))

    form = NewPostForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data["content"]
        Post.objects.create(content=content, creator=request.user)
    else:
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="network/login.html")
def edit_post_view(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))

    data = json.loads(request.body)
    content = data.get("content")
    pk = data.get("pk")
    try:
        post = Post.objects.get(
            pk=pk, creator=request.user
        )  # Only user can edit own messages
        post.content = content
        post.edited = True
        post.save()
    except Exception as e:
        print(e)
        return JsonResponse(
            {"error": "Only creator allowed to edit posts."}, status=400
        )
    return JsonResponse({"message": "Succesfully edited message."}, status=200)


@login_required(login_url="network/login.html")
def like_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    pk = data.get("pk")
    try:
        post = Post.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Post does not exist."}, status=404)
    # Create like only when needed
    # Probably better to delete object when unliked, idk
    try:
        like = Like.objects.get(post=post, creator=request.user)
        like.liked = not like.liked  # Reverse, like -> dislike, dislike -> like
        like.save()

    except:  # Like doesn't exist
        like = Like.objects.create(liked=True, post=post, creator=request.user)
        like.save()

    return JsonResponse(
        {"body": f"Post {'like' if like.liked else 'dislike'} succesfull."},
        status=201,
    )


def user_page(request, user: str):
    user = User.objects.get(username=user)
    posts = user.posts.all()
    paginator = Paginator(posts, 10)  # Show 10 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/user.html", {"profile": user, "page_obj": page_obj})


@login_required(login_url="network/login.html")
def follow_user_view(request, user: str):
    profile = User.objects.get(username=user)
    following = request.user.following
    if profile == request.user:
        return HttpResponseRedirect(reverse("profile", kwargs={"user": profile}))
    if profile in following.all():
        following.remove(profile)
        print(f"{request.user} UNFOLLOWED {profile}")
    else:
        following.add(profile)
        print(f"{request.user} FOLLOWED {profile}")

    return HttpResponseRedirect(reverse("profile", kwargs={"user": profile}))


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
