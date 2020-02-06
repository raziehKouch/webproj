from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from . import views
from .models import post
urlpatterns = [
    path('home', views.home , name='blog-home'),
    path('channels', views.channel , name='blog-channel'),
    path('newChannel', views.newChannel , name='newChannel'),
    path('channels/<int:pk>/edit/', views.edit_channel, name='edit_channel'),
    path('channels/<int:pk>/editpost/', views.edit_post, name='edit_post'),
    path('channels/<int:id>/channel_detail', views.channel_detail, name='channel_detail'),
    path('channels/<int:pk>/newPost', views.newPost, name='newPost'),
    path('channels/<int:id>/delete_channel', views.delete_channel, name='delete_channel'),
    path('channels/<int:id>/delete_post', views.delete_post, name='delete_post'),
    path('view_post/<int:p_pk>', views.view_post, name='view_post'),
    path('view_post_c/<int:id>', views.comment_thread, name='comment_thread'),
    # path('channels/<int:ch_pk>/like_post/<int:p_pk>/', views.like_post, name='like_post'),
    path('channels/<int:id>/subAuthor', views.subAuthor, name='subAuthor'),
    path('channels/<int:id>/addAuthor', views.addAuthor, name='addAuthor'),
    path('channels/<int:id>/addAuthors', views.addAuthors, name='addAuthors'),
    path('channels/<int:chID>/addAuthorNow/<int:uID>', views.addAuthorNow, name='addAuthorNow'),
    path('channels/<int:chID>/subAuthorNow/<int:uID>', views.subAuthorNow, name='subAuthorNow'),
# {% url 'addAuthorNow' chID=channel.pk uID=u.id %}
    path('channels/<int:chID>/followChannel/<int:uID>', views.followChannel, name='followChannel'),
    path('search', views.search, name='search'),
    path('notification', views.notification, name='notification'),
    path('view_post/<int:p_pk>/like/', views.postliketoggle.as_view(), name='like'),
    path('view_post/<int:p_pk>/apilike/', views.PostLikeToggleAPI.as_view(), name='like-api'),
    path('view_post/<int:p_pk>/dislike/', views.postDisliketoggle.as_view(), name='dislike'),
    path('view_post/<int:p_pk>/apidislike/', views.PostDisLikeToggleAPI.as_view(), name='dislike-api'),
]