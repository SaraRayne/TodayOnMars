from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django import forms
import requests
import json
import random
import os

from .models import User, Thread, Category, Reply
# Create your views here.

# Consult README for API key
API_KEY = os.environ.get('NASA_API')

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.CheckboxSelectMultiple,
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            "reply": ""
        }


""" Main page of application """
def index(request):

    # Get weather
    # API retrieved from source code of: https://mars.nasa.gov/mars2020/weather/
    f = r"https://mars.nasa.gov/rss/api/?feed=weather&category=mars2020&feedtype=json"
    data = requests.get(f)
    a = json.loads(data.text)

    # Retrieves oldest first, will always be approx. 7 days behind
    sol = a['sols'][0]['sol']
    earth = a['sols'][0]['terrestrial_date']

    # Calculates average temperature given min and max temps of the day
    average = ((a['sols'][0]['min_temp']) + (a['sols'][1]['max_temp'])) / 2

    # retrieve three most recent forum posts
    threads = Thread.objects.all()
    threads = threads.order_by("-date").all()[:3]

    return render(request, "mars/index.html", {
        "threads": threads,
        "sol": sol,
        "earth": earth,
        "average": average
    })


""" Handles creation of new thread posts
and renders forums page """
def forums(request):

    # Handles creation of new thread
    if request.method == "POST":

        # Retrieve form data, check for validity
        # Then retrieve logged-in user before saving
        form = ThreadForm(request.POST)
        if form.is_valid():
            # Before saving thread, retrieve current user
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            # Saves category after saving to database
            form.save_m2m()

            # Go to newly created thread page
            return redirect('thread', thread_id=thread.id)

        # If form is not valid, reload forums page
        else:
            return redirect('forums')

    # Renders forums page
    else:
        categories = Category.objects.all()

        threads = Thread.objects.all()
        threads = threads.order_by("-date").all()
        return render(request, "mars/forums.html", {
            "threads": threads,
            "form": ThreadForm(),
            "categories": categories
        })


""" Retrieves and renders individual thread page """
def thread(request, thread_id):

    # Find thread matching selected thread id
    thread = Thread.objects.get(id=thread_id)

    # Retrieve replies for that thread
    replies = Reply.objects.filter(thread=thread)

    return render(request, "mars/thread.html", {
            "thread": thread,
            "form": ReplyForm(),
            "replies": replies
    })


""" Filters threads by category and renders matches """
def filter(request, category):
    # Get category to filter by
    category = Category.objects.get(category=category)

    # Get threads in selected category, order by newest
    threads = Thread.objects.filter(category=category)
    threads = threads.order_by("-date").all()

    # Get all categories for button
    categories = Category.objects.all()

    return render(request, "mars/forums.html", {
        "threads": threads,
        "form": ThreadForm(),
        "categories": categories
    })


""" Handles creation of new reply to thread """
def reply(request, thread_id):
    # Retrieve form data, check for validity
    # Then retrieve logged-in user before saving
    form = ReplyForm(request.POST)
    if form.is_valid():

        # Get thread it's a reply to
        thread = Thread.objects.get(id=thread_id)

        # Before saving reply, retrieve current user
        reply = form.save(commit=False)
        reply.author = request.user
        reply.thread = thread
        reply.save()

        return redirect('thread', thread_id=thread_id)

    else:
        return render(request, "mars/thread.html", {
            "thread": thread,
            "form": form
        })


""" Retrieves an image from NASA Mars Rover API """
def image(request):

    # Choose a random number for the date to search
    date = random.randint(1, 1000)

    # Set parameters, random data and API key
    params = {"sol": date, "api_key": API_KEY}
    # API path
    f = r"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?"
    data = requests.get(f, params = params)
    a = json.loads(data.text)

    # Find number of photos in API call data
    maximum = len(a["photos"])

    # If there are no photos for a particular day, query again
    while maximum == 0:
        date = random.randint(1, 1000)
        params = {"sol": date, "api_key": API_KEY}
        data = requests.get(f, params = params)
        a = json.loads(data.text)
        maximum = len(a["photos"])

    # If day has photos, choose one photo at random
    pic = random.randint(1, maximum)

    # Retrieve the image
    try:
        image = a["photos"][pic]["img_src"]
    # If there's an index issue, render error image
    except IndexError:
        print("Out of range")
        image = "static/mars/no_image.svg.png"

    return render(request, "mars/images.html", {
        "image": image
    })


""" Handles forum search, returns matching threads """
def search(request):

    if request.method == "POST":

        # Get query
        query = request.POST['q']

        # Retrieve all threads
        threads = Thread.objects.all()

        # Placeholder list for results that match
        results = []

        # Loop over threads to search for query
        for thread in threads:
            # Check for query in title
            if query.lower() in thread.title.lower():
                results.append(thread)
            # Check for query in thread body
            elif query.lower() in thread.content.lower():
                results.append(thread)
            else:
                print("Not in")

        # Retrieve categories for page render
        categories = Category.objects.all()

        return render(request, "mars/forums.html", {
            "threads": results,
            "form": ThreadForm(),
            "categories": categories
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
            return render(request, "mars/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mars/login.html")


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
            return render(request, "mars/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mars/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mars/register.html")
