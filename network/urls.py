
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("editpost/<int:post_id>", views.editpost, name="editpost"),
    path("allpost/<str:posts>", views.allpost, name="allpost"),
    path("<str:user>", views.profile, name="profile")
]

