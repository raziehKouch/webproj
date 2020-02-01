from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home , name='blog-home'),
    path('channels', views.channel , name='blog-channel'),
    path('newChannel', views.newChannel , name='newChannel'),
    path('channels/<int:pk>/edit/', views.edit_channel, name='edit_channel'),
    path('channels/<int:pk>/editpost/', views.edit_post, name='edit_post'),
    path('channels/<int:pk>/viewPosts', views.viewPosts, name='viewPosts'),
    path('channels/<int:pk>/newPost', views.newPost, name='newPost'),
    path('channels/<int:id>/delete_channel', views.delete_channel, name='delete_channel'),
    path('channels/<int:id>/addMember', views.addMember, name='addMember'),
    path('search', views.search, name='search'),
]