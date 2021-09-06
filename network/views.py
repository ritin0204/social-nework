from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

from .models import User,Post,Follow


def index(request):
    allposts = Post.objects.all()
    allposts = allposts.order_by("-created_at").all()
    paginator = Paginator(allposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "allpost": allposts
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

@csrf_exempt
@login_required(login_url='/login/')
def newpost(request):
    #check method is post or not
    if request.method !="POST":
        return JsonResponse({"Error": "POST request required"},status=400)
    text = request.body
    #check for empty text area
    if text == [""]:
        return JsonResponse({
            "error": "at least 5 or more words required"
        },status=400)
    post = Post(
        text = text.decode('utf-8'),
        user_id = request.user
    )
    post.save()
    return JsonResponse({"message": "post submitted"},status=201)


def allpost(request, posts):
    if posts == "following":
        userid=request.user
        p = Follow.objects.get(c_user = userid).user_data()
        allpost = Post.objects.filter(user_id__in = p["following"]).distinct()
    else:
        return JsonResponse({"error":"invailiad posts"},status=400)
    allpost = allpost.order_by("-created_at").all()
    return render(request, "network/index.html", {
        "allpost": allpost
     })

@csrf_exempt
@login_required(login_url='/login/')
def profile(request,user):
    user = str(user)
    if request.method == "POST":
        data = json.loads(request.body)
        if request.user.username == user:
            return JsonResponse({"error":"You Can't Follow/UnFollow Yourself"},status=400)
        elif data.get("Follow") is not None:
            userdata = Follow.objects.get(c_user=request.user)
            ac_user = User.objects.get(username= user)
            userdata.following.add(ac_user)
            userdata.save()
            flwr_user = Follow.objects.get(c_user=ac_user)
            flwr_user.followers.add(request.user)
            flwr_user.save()
            return JsonResponse({"message":"Followed Successfully"},status=201)
        elif data.get("Unfollow") is not None:
            userdata = Follow.objects.get(c_user=request.user)
            ac_user = User.objects.get(username= user)
            userdata.following.remove(ac_user)
            userdata.save()
            flwr_user = Follow.objects.get(c_user=ac_user)
            flwr_user.followers.remove(request.user)
            flwr_user.save()
            return JsonResponse({"message":"Unfollowed Successfully"},status=201)
        else:
            return JsonResponse({"error":"Invaild post Request"},status=400)
    if request.method =="GET":
        userdata = User.objects.get(username=user)
        try:
            usr_data = Follow.objects.get(c_user=userdata).user_data()
            following = len(usr_data["following"])
            follower = len(usr_data["followers"])
        except:
            usr_data =Follow()
            usr_data.c_user = userdata
            usr_data.save()
        if usr_data["followers"] is None:
            message=0
        elif request.user.id in usr_data["followers"]:
            message = 1
        elif request.user == userdata:
            message =2
        else:
            message = 0
        try:
            posts = Post.objects.filter(user_id = userdata)
            posts = posts.order_by("-created_at").all()
        except:
            return render(request, "network/profile.html", {
           "usr_email": userdata,
           "follower": follower,
           "following": following,
           "message": message
            })
        return render(request, "network/profile.html", {
           "usr_email": userdata,
           "follower": follower,
           "following": following,
           "message": message,
           "posts": posts
        })

@csrf_exempt
@login_required(login_url='/login/')
def editpost(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        return JsonResponse({"error": "post not found"}, status=404)

    if request.method== "GET":
        return JsonResponse(post.serialize())

    elif request.method == "POST":
        if request.user != post.user_id:
            return JsonResponse({"error": "You can't Edit someone else post"}, status=401)
        text = request.body
    #check for empty text area
        if text == [""]:
            return JsonResponse({
            "error": "at least 5 or more words required"
            },status=400)
        postw = Post.objects.get(pk=post_id)
        postw.text = text.decode('utf-8')
        postw.save()
        posts = Post.objects.get(pk=post_id)
        return JsonResponse(posts.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes+=1
        if data.get("unlikes") is not None:
            post.unlikes+=1
        post.save()
        posts = Post.objects.get(pk=post_id)
        return JsonResponse(posts.serialize())

    else:
        return JsonResponse({"error": "Method not found"}, status=400)


    
