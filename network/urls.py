from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:user>", views.user_page, name="profile"),
    # API Routes
    path("posts/like", views.like_post, name="like"),
    path("posts/edit_post", views.edit_post_view, name="edit_post"),
    path("posts/create_post", views.create_post_view, name="create_post"),
    path("user/<str:user>/follow", views.follow_user_view, name="follow"),
]
