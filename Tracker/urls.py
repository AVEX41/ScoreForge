from django.urls import path

from . import views

urlpatterns = [
    # --- HTML response ---
    path("", views.index, name="index"),
    # --- JSON response ---
    path("data/index/fav", views.indexDataFav, name="indexData"),
    path("data/manage", views.manage, name="manage"),
    path("data/manage/<str:view>", views.manageView, name="manageView"),
    # --- form submission ---
    # new
    path("form/new", views.new, name="new"),
    path("form/comp-new", views.comp_new, name="comp_new"),
    # edit
    path("form/edit", views.edit, name="edit"),
    path("form/comp-edit", views.comp_edit, name="comp_edit"),
    # delete
    path("form/delete", views.delete, name="delete"),
    path("form/comp-delete", views.comp_delete, name="comp_delete"),
    # user edit
    path("form/edit/usr/name", views.usr_name, name="usr_name"),
    path("form/edit/usr/usrname", views.usr_usrname, name="usr_usrname"),
    path("form/edit/usr/email", views.usr_email, name="usr_email"),
    path("form/edit/usr/pword", views.usr_pword, name="usr_pword"),
    # Favourite
    path("form/fav", views.indexFav, name="indexFav"),
    # --- Handle login ---
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
