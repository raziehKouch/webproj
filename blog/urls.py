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
    path('channels/<int:id>/Channeldetail', views.channel_detail, name='channel_detail'),
    path('channels/<int:pk>/newPost', views.newPost, name='newPost'),
    path('channels/<int:id>/delete_channel', views.delete_channel, name='delete_channel'),
    path('channels/<int:id>/delete_post', views.delete_post, name='delete_post'),
    path('view_post/<int:p_pk>', views.view_post, name='view_post'),
    path('channels/<int:id>/addMember', views.addMember, name='addMember'),
    path('search', views.search, name='search'),
    path('notification', views.notification, name='notification'),
    path('view_post/<int:p_pk>/like/', views.postliketoggle.as_view(), name='like'),
    path('view_post/<int:p_pk>/apilike/', views.PostLikeToggleAPI.as_view(), name='like-api'),
]