
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>", views.profile, name="profile"),
    path("<int:post_id>", views.like, name="like"),

    # API
    path('like/<int:post_id>', views.like, name="like"),
    path('likes/<int:post_id>', views.likes_count, name="likes"),
    path('likers/<int:post_id>', views.likers, name="likers"),
    path('user/<int:user_id', views.user, name="user")
]
