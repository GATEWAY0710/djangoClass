from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("create", views.create, name="create"),
    path("list", views.list, name="list"),
    path("view/<student_id>", views.view, name="view"),
    path("delete/<student_id>", views.delete, name="delete")
]