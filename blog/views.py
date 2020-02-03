import json
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import post, Chanel, is_author
from .forms import channelForm, PostForm
from django.contrib import messages
from django.utils import timezone
from django.views.generic import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from users.models import profile




def home(request):
    # following_post_authors = request.user.profile.get_followers(request.user)
    # print(following_post_authors)
    # following_post_channels =
    # followed = post.objects.filter(author__in = following_post_authors)
    followed = post.objects.filter()
    time_threshold = timezone.now() - timezone.timedelta(days=7)
    recent = post.objects.all().order_by('-date_posted')
    hot = post.objects.filter(date_posted__gt=time_threshold)#todo.order_('-likes')
    contributed = post.objects.all()#todo
    context = {
        'followed' : followed,
        'recent' : recent,
        'hot' : hot,
        'contributed' : contributed,
    }
    return render(request, 'blog/home.html', context)


def channel(request):
    context = {
        'channels': Chanel.objects.all()
    }
    return render(request, 'blog/channel.html', context)

def newChannel(request):
    if request.method == "POST":
        form = channelForm(request.POST)
        if form.is_valid():
            ch = form.save(commit=False)
            ch.admin = request.user
            ch.save()

            return HttpResponseRedirect('channels', messages.success(request, 'Channel created.'))
    else:
        form = channelForm()
    return render(request, 'blog/newChannel.html', {'form': form})

def newPost(request,pk):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            ch = form.save(commit=False)
            ch.author = request.user
            c = Chanel.objects.get(id = pk)
            ch.save()
            print("@@@@@@@@@@@@@@@@@@@ before",c,ch.chanel)
            ch.chanel = c
            ch.save()
            print("@@@@@@@@@@@@@@@@@@@",c,ch.chanel)

            return HttpResponseRedirect('channel_detail', messages.success(request, 'Post created.'))
    else:
        form = PostForm()
    return render(request, 'blog/newPost.html', {'form': form})


def edit_channel(request, pk):
    ch = get_object_or_404(Chanel, pk=pk)
    if request.method == "POST":
        form = channelForm(request.POST, instance=ch)
        if form.is_valid():
            ch = form.save(commit=False)
            ch.author = request.user
            ch.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next, messages.success(request, 'Channel updated.'))


    else:
        form = channelForm(instance=ch)
    return render(request, 'blog/edit_channel.html', {'form': form})

def edit_post(request, pk):
    ch = get_object_or_404(post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=ch)
        if form.is_valid():
            ch = form.save(commit=False)
            ch.author = request.user
            ch.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next, messages.success(request, 'Post updated.'))
    else:
        form = PostForm(instance=ch)
    return render(request, 'blog/edit_post.html', {'form': form})


def channel_detail(request, id):
    c = Chanel.objects.get(id = id)
    posts = post.objects.filter(chanel=c)
    channel_auths = Chanel.get_channel_auths(c)
    context = {
        'c' : c,
        'posts': posts,
        'ch_pk': id,
        'channel_auths' : channel_auths,
    }
    return render(request, 'blog/channel_detail.html', context)

def delete_channel(request, id, pk):
    Chanel.objects.filter(id=id).delete()
    next = request.POST.get('next', '/channels')
    return HttpResponseRedirect(next)

def delete_post(request, id, pk=None):
    post.objects.filter(id=id).delete()
    if pk:
        return render(request, 'blog/channel_detail.html', {'ch_pk':pk})
    return #todo

def view_post(request, p_pk):
    mypost= post.objects.filter(id = p_pk)
    resp = {'shared_url' : f'127.0.0.1/view_post/{p_pk}',
            'post': mypost[0]
            }
    return render(request, 'blog/view_posts.html', resp)

def addAuthor(request, id):
    context = {
        'channel' : Chanel.objects.get(id = id),
    }
    return render(request, 'blog/addAuthor.html', context )

def addAuthors(request, id):
    query = request.GET.get('q')
    show_users = User.objects.filter(username__icontains=query)
    context = {
        'channel' : Chanel.objects.get(id = id),
        'show_users' : show_users,
    }
    return render(request, 'blog/addAuthors.html', context )

def addAuthorNow(request, chID, uID):
    channel = Chanel.objects.get(id = chID),
    auth = User.objects.get(id = uID),
    if is_author.objects.filter(author=auth, channel=channel).count() == 0:
        is_author.objects.create(author=auth, channel=channel)
        messages.success(request, f'New author added!')

def search(request):
    query = request.GET.get('q')
    search_posts = post.objects.filter(title__icontains=query)
    search_users = User.objects.filter(username__icontains=query)
    search_channels = Chanel.objects.filter(title__icontains=query)
    context = {
        'query': query,
        'search_posts': search_posts,
        'search_users': search_users,
        'search_channels': search_channels,
    }
    return render(request, 'blog/search.html', context)

def notification(request):
    return render(request, 'blog/notification.html', {})


class postliketoggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(post, pk=kwargs['p_pk'])
        likeurl = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            print('im in first if')
            if user in obj.likes.all():
                print('im in sec1 if')
                obj.likes.remove(user)
            else:
                print('im in sec2 if')
                obj.likes.add(user)
        return likeurl


class postliketoggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(post, pk=kwargs['p_pk'])
        likeurl = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            print('im in first if')
            if user in obj.likes.all():
                print('im in sec1 if')
                obj.likes.remove(user)
            else:
                print('im in sec2 if')
                obj.likes.add(user)
        return likeurl



class PostLikeToggleAPI(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, p_pk=None, format=None):
        obj = get_object_or_404(post, pk=p_pk)
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            'updated': updated,
            'liked': liked,
            'count': obj.likes.count()
        }
        return Response(data)