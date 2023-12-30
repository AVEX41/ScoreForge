from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse


from .models import User, CompetitionType, Competition


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user

    return render(
        request,
        "Tracker/index.html",
        {"user": user},
    )


def indexDataFav(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user

    score_table = user.competitionTypes.get(user_favourite=True)

    if score_table:
        # Serialize the score sets associated with the score table
        serialized_competitions = score_table.serialize_competition_type()

        # Create a JSON response
        response_data = {
            "score_table_id": score_table.id,
            "score_table_name": score_table.name,
            "score_sets": serialized_competitions,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "No table favourited"})


def setData(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user
    score_set = user.competitionTypes.competitions.all()

    if score_set:
        pass

    return HttpResponseRedirect(reverse("login"))


def manage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user
    competition_types = user.serialize_competitions()

    return JsonResponse({"competition_types": competition_types})


def manageView(request, view):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user

    try:
        score_table = user.competitionTypes.get(id=view)
        score = score_table.serialize_competition_type()
    except CompetitionType.DoesNotExist:
        return JsonResponse({"error": "Invalid competition type."})

    responseData = {
        "competition_type_id": score_table.id,
        "competition_type_name": score_table.name,
        "competition_type_description": score_table.description,
        "competition_type_shots_count": score_table.shots_count,
        "competitions": score,
    }

    return JsonResponse(responseData)


def new(request):
    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"error": "Invalid data."})

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"error": "Invalid user."})

        try:
            # Create new competition type
            competition_type = CompetitionType(
                user=user,
                name=data["name"],
                description=data["description"],
                shots_count=data["shot_count"],
                user_favourite=False,
            )
            competition_type.save()
        except KeyError:
            return JsonResponse({"error": "Invalid competition type data."})

        return JsonResponse({"message": "Competition type created successfully."})
    else:
        return JsonResponse({"error": "POST request required."})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
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
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(
                request, "Tracker/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Tracker/register.html")
