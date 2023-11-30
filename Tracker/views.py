from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse


from .models import User, ScoreTable, ScoreSet, ScoreNode


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user

    return render(
        request,
        "Tracker/index.html",
        {"user": user},
    )


def indexData(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user

    # Assuming you have a ScoreTable instance for the current user
    score_table = user.score_tables.first()

    if score_table:
        # Serialize the score sets associated with the score table
        serialized_score_sets = score_table.serialize_score_sets()

        # Create a JSON response
        response_data = {
            "score_table_id": score_table.id,
            "score_sets": serialized_score_sets,
            # Add other data you want to include in the JSON response
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "No score table found for the user"})


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
                "Tracker/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "Tracker/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "Tracker/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "Tracker/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Tracker/register.html")
