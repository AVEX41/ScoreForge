from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse


from .models import User, PerformanceIndicator, DataPoint


# -- HTML response --
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user

    return render(
        request,
        "Tracker/index.html",
        {"user": user},
    )


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


# -- JSON response --
def indexDataFav(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method != "GET":
        return HttpResponseBadRequest("Need to use get")

    user = request.user
    try:
        perf_indicator = user.performance_indicators.get(user_favourite=True)
    except PerformanceIndicator.DoesNotExist:
        return JsonResponse({"message": "No Performance indicator favourited."})

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
        return JsonResponse({"message": "No Performance indicator favourited."})


def manage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method != "GET":
        return HttpResponseBadRequest("Need to use get")

    user = request.user
    performance_indicators = user.serialize_performance_indicators()

    return JsonResponse({"competition_types": performance_indicators})


def manageView(request, view):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method != "GET":
        return HttpResponseBadRequest("Need to use get")

    user = request.user

    try:
        perf_indicator = user.performance_indicators.get(id=view)
        data_points = perf_indicator.serialize_performance_indicator()
    except PerformanceIndicator.DoesNotExist:
        return JsonResponse({"message": "Invalid Performance indicator."}, status=400)

    responseData = {
        "performance_indicator_id": perf_indicator.id,
        "performance_indicator_name": perf_indicator.name,
        "performance_indicator_description": perf_indicator.description,
        "data_points": data_points,
    }

    return JsonResponse(responseData)


# -- Form submissions --
def new(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, status=400)

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
                {"message": "Invalid performance indicator data."}, status=400
            )

        return JsonResponse(
            {"message": "Performance indicator created successfully."}, status=200
        )
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def comp_new(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, staus=400)

        try:
            # Get score table
            perf_indicator = PerformanceIndicator.objects.get(
                id=data["competition_type"]
            )
        except KeyError:
            return JsonResponse(
                {"message": "Invalid perfomance indicator."}, status=400
            )

        try:
            # Create new competition type
            competition = DataPoint(
                score_table=perf_indicator,
                score=data["score"],
            )

            competition.save()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data point data. Wrong parameters."}, status=400
            )

        return JsonResponse({"message": "Datapoint created successfully."}, status=200)
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def edit(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, status=400)

        try:
            # Get object
            performance_indicator = PerformanceIndicator.objects.get(
                id=data["submit-type"], user=user
            )
        except:
            return JsonResponse(
                {
                    "message": "Could not find a Perfomance indicator with the specified ID and user."
                },
                status=400,
            )
        try:
            # Edit object
            performance_indicator.name = data["name"]
            performance_indicator.description = data["description"]

            performance_indicator.save()
        except:
            return JsonResponse(
                {"message": "Invalid performance indicator data."}, status=400
            )

        return JsonResponse(
            {"message": "Performance indicator edited successfully."}, status=200
        )
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def comp_edit(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, staus=400)

        try:
            data_point = DataPoint.objects.get(id=data["submit_type"])
            perf_indicator = data_point.score_table
            data_point_user = perf_indicator.user

            if data_point_user != user:
                raise DataPoint.DoesNotExist()

            # Edit data point
            # data_point = DataPoint.objects.get(id=data["submit_type"])

            data_point.score = data["score"]

            data_point.save()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data point data. Wrong parameters."}, status=400
            )
        except DataPoint.DoesNotExist:
            return JsonResponse(
                {
                    "message": "Could not find a datapoint with the specified id and user."
                },
                status=400,
            )
        except:
            return JsonResponse(
                {"message": "Invalid data, the declaration did not work."}, status=400
            )

        return JsonResponse({"message": "Datapoint edited successfully."}, status=200)
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def delete(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, status=400)

        try:
            # Get object
            performance_indicator = PerformanceIndicator.objects.get(
                id=data["item"], user=user
            )

            # delete
            performance_indicator.delete()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid performance indicator data."}, status=400
            )
        except PerformanceIndicator.DoesNotExist:
            return JsonResponse(
                {
                    "message": "Did not find a performance indicator with the specified user and id."
                },
                status=400,
            )

        return JsonResponse(
            {"message": "Performance indicator deleted successfully."}, status=200
        )
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def comp_delete(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, staus=400)

        try:
            data_point = DataPoint.objects.get(id=data["item"])
            perf_indicator = data_point.score_table
            data_point_user = perf_indicator.user

            if data_point_user != user:
                raise DataPoint.DoesNotExist()

            # Edit data point
            data_point = DataPoint.objects.get(id=data["item"])

            # delete
            data_point.delete()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data point data. Wrong parameters."}, status=400
            )
        except DataPoint.DoesNotExist:
            return JsonResponse(
                {
                    "message": "Could not find a datapoint with the specified id and user."
                },
                status=400,
            )

        return JsonResponse({"message": "DataPoint deleted successfully."}, status=200)
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def indexFav(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)
        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, staus=400)
        try:
            indicators = user.performance_indicators.filter(user_favourite=True)

            for indicator in indicators:
                indicator.user_favourite = False

            new_fav = user.performance_indicators.get(id=data["perf_id"])
            new_fav.user_favourite = True

            for indicator in indicators:
                indicator.save()
            new_fav.save()
            user.save()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data point data. Wrong parameters."}, status=400
            )
        except PerformanceIndicator.DoesNotExist:
            return JsonResponse(
                {
                    "message": "Did not find a performance indicator with the specified user and id."
                },
                status=400,
            )

        return JsonResponse({"message": "Favourite edited successfully."}, status=200)
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def usr_name(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)
        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, staus=400)
        try:
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]

            user.save()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data. Wrong parameters."}, status=400
            )
        return JsonResponse({"message": "User edited successfully."}, status=200)
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def usr_usrname(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)

        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, staus=400)

        try:
            if User.objects.filter(username=data["user_name"]).exists():
                return JsonResponse({"message": "Username already taken."}, status=400)
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data. Wrong parameters."}, status=400
            )
        except:
            return JsonResponse({"message": "Username already taken."}, status=400)

        try:
            user.username = data["user_name"]

            user.save()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data. Wrong parameters."}, status=400
            )
        except:
            return JsonResponse({"message": "Username already taken."}, status=400)

        return JsonResponse({"message": "User edited successfully."}, status=200)

    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def usr_email(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)
        try:

            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, staus=400)
        try:
            # Check if already in use
            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "Email already in use."}, status=400)

            user.email = data["email"]

            user.save()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data point data. Wrong parameters."}, status=400
            )
        return JsonResponse({"message": "User edited successfully."}, status=200)
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


def usr_pword(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Must be logged in."}, status=400)

    if request.method == "POST":
        try:
            # Get data from request
            data = request.POST
        except KeyError:
            return JsonResponse({"message": "Invalid data."}, status=400)
        try:
            # Get user
            user = request.user
        except KeyError:
            return JsonResponse({"message": "Invalid user."}, staus=400)
        try:
            user.set_password(data["password"])

            user.save()
        except KeyError:
            return JsonResponse(
                {"message": "Invalid data point data. Wrong parameters."}, status=400
            )
        return JsonResponse({"message": "User edited successfully."}, status=200)
    else:
        return JsonResponse({"message": "POST request required."}, status=400)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
