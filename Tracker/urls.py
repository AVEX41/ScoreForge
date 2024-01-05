from django.urls import path

from . import views

urlpatterns = [
    # HTML response
    path("", views.index, name="index"),
    # JSON response
    path("data/index/fav", views.indexDataFav, name="indexData"),
    path("data/manage", views.manage, name="manage"),
    path("data/manage/<str:view>", views.manageView, name="manageView"),
    # form submission
    path("form/new", views.new, name="new"),
    path("form/comp-new", views.comp_new, name="comp_new"),
    # Handle login
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
