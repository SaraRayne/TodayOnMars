from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("forums", views.forums, name="forums"),
    path("image", views.image, name="image"),
    path("<int:thread_id>", views.thread, name="thread"),
    path("<int:thread_id>/reply", views.reply, name="reply"),
    path("<str:category>/category", views.filter, name="filter"),
    path("search", views.search, name="search"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
