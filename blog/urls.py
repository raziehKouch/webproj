from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home , name='blog-home'),
    path('channels', views.channel , name='blog-channel'),
    path('newChannel', views.newChannel , name='newChannel'),
    path('channels/<int:pk>/edit/', views.edit_channel, name='edit_channel'),
    path('channels/<int:pk>/viewPosts', views.viewPosts, name='viewPosts'),
    path('channels/<int:pk>/newpost', views.newPost, name='newPost'),
    path('channels/<int:id>/delete_channel', views.delete_channel, name='delete_channel'),
    path('channels/<int:id>/addMember', views.addMember, name='addMember'),

]