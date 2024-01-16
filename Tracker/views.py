from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse


from .models import User, PerformanceIndicator, DataPoint


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
    try:
        perf_indicator = user.performance_indicators.get(user_favourite=True)
    except PerformanceIndicator.DoesNotExist:
        return JsonResponse({"error": "No table favourited"})

    if perf_indicator:
        # Serialize the score sets associated with the score table
        serialized_competitions = perf_indicator.serialize_performance_indicator()

        # Create a JSON response
        response_data = {
            "perf_indicator_id": perf_indicator.id,
            "perf_indicator_id": perf_indicator.name,
            "perf_indicator": serialized_competitions,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "No table favourited"})


def manage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user
    performance_indicators = user.serialize_performance_indicators()

    return JsonResponse({"competition_types": performance_indicators})


def manageView(request, view):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user

    try:
        perf_indicator = user.performance_indicators.get(id=view)
        data_points = perf_indicator.serialize_performance_indicator()
    except PerformanceIndicator.DoesNotExist:
        return JsonResponse({"error": "Invalid competition type."})

    responseData = {
        "performance_indicator_id": perf_indicator.id,
        "performance_indicator_name": perf_indicator.name,
        "performance_indicator_description": perf_indicator.description,
        "data_points": data_points,
    }

    return JsonResponse(responseData)


def new(request):
    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"error": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"error": "Invalid user."}, status=400)

        try:
            # Create new competition type
            performance_indicator = PerformanceIndicator(
                user=user,
                name=data["name"],
                description=data["description"],
                user_favourite=False,
            )
            performance_indicator.save()
        except KeyError:
            return JsonResponse(
                {"error": "Invalid performance indicator data."}, status=400
            )

        return JsonResponse(
            {"message": "performance indicator created successfully."}, status=200
        )
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def comp_new(request):
    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"error": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"error": "Invalid user."}, staus=400)

        try:
            # Get score table
            perf_indicator = PerformanceIndicator.objects.get(
                id=data["competition_type"]
            )
        except KeyError:
            return JsonResponse({"error": "Invalid score table."}, status=400)

        try:
            # Create new competition type
            competition = DataPoint(
                score_table=perf_indicator,
                score=data["score"],
            )

            competition.save()
        except KeyError:
            return JsonResponse(
                {"error": "Invalid data point data. Wrong parameters"}, status=400
            )

        return JsonResponse(
            {"message": "Competition created successfully."}, status=200
        )
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def edit(request):
    ...


def comp_edit(request):
    ...


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
