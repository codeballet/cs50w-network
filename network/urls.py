
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API
    path('api/like/<int:post_id>', views.like_api, name="like_api"),
    path('api/likes/<int:post_id>', views.likes_count_api, name="likes_api"),
    path('api/likers/<int:post_id>', views.likers_api, name="likers_api"),
    path('api/follow/<int:user_id>', views.follow_api, name="follow_api"),
    path('api/followed/<int:user_id>', views.followed_api, name="followed_api"),
    path('api/followers/<int:user_id>',
         views.followers_api, name="followers_api"),
    path('api/following/<int:user_id>',
         views.following_api, name="following_api"),
    path('api/unfollow/<int:user_id>', views.unfollow_api, name="unfollow_api"),
    path('api/update/<int:user_id>/<int:post_id>',
         views.update_api, name="update_api")
]
