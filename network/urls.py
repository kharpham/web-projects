
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("posts/<str:profile>", views.posts_api, name="posts_api"),
    path("post/<int:id>", views.post, name="post"),
    path("interact_post/<int:id>", views.interact_post, name="interact_post"),
]


