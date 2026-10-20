from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("", include("django.contrib.auth.urls")), 
    path("me/", views.my_posts, name="my_posts"),
    path("new/", views.new_post, name="new_post"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
]