
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # User administration management
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # Post Management
    path("create_post", views.create_post, name="create_post"),
    path("view_post/<int:id>", views.view_post, name="view_post"),
    path("followed/", views.followed, name="followed"),
        #path("view_post/liked/<int:id>", views.like_post, name="like_post"),
        #path("view_post/disliked/<int:id>", views.like_post, name="dislike_post"),
        
    # API Post Management
    path("api/posts/<int:id>/", views.JS_get_post, name="js_get_post"),
    path("api/posts/<int:id>/like/", views.JS_like_post, name="js_like_post"),
    path("api/posts/<int:id>/dislike/", views.JS_dislike_post, name="js_dislike_post"),
    path("api/posts/<int:id>/like-dislike/", views.JS_get_like_dislike, name="js_get_like_dislike"),
    path("api/posts/<int:id>/edit/", views.JS_edit_post, name="JS_edit_post"),
    
    # User Management
    path("userpage/<str:user>", views.userpage, name="userpage"),
    path("follow/<str:user>", views.follow_user, name="follow_user"),
    path("unfollow/<str:user>", views.unfollow_user, name="unfollow_user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)