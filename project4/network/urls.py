from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("postsubmit", views.post_submit, name="postsubmit"),
    path("allposts", views.all_posts, name="allposts"),
    path("profile", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("like", views.like, name="like"),
    path("edit", views.edit, name="edit")
]
