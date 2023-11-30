from django.urls import path

from . import views

urlpatterns = [
    # HTML response
    path("", views.index, name="index"),
    # JSON response
    path("data/index", views.indexData, name="indexData"),
    # Handle login
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
