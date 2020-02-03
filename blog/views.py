import json

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import post, Chanel
from .forms import channelForm, PostForm
from django.contrib import messages
from django.utils import timezone

from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType

from .models import  Like


def likePost(request):
    print("jjjjjjjjjjjjjjjjjjjjjjjjjjj")
    if request.method == 'GET':

        post_id = request.GET['post_id']
        likedpost = post.obejcts.get(pk=post_id)  # getting the liked posts
        print("llllllllllllllllllll", likedpost)
        m = Like(post=likedpost)  # Creating Like Object
        print("mmmmmmmmmmmmmmmmmm", m)
        m.save()  # saving it to store in database
        return HttpResponse("Success!")  # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")


def home(request):
    time_threshold = timezone.now() - timezone.timedelta(days=7)
    followed = post.objects.all()#todo
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

# def like_post(request, val, p_pk , ch_pk):
#     mypost = post.objects.filter(id=p_pk)
#     if val==1:
#         mypost.like = 1
#     elif val==2:
#         mypost.dislike =1
#     mypost.save()
#     resp = {'shared_url' : f'127.0.0.1/channels/{ch_pk}/view_post/{p_pk}',
#             'ch_pk':ch_pk,
#             'p_pk':p_pk,
#             'post': mypost,
#             }
#     return render(request, 'blog/view_post.html',resp)




def view_post(request, p_pk):
    mypost= post.objects.filter(id = p_pk)
    resp = {'shared_url' : f'127.0.0.1/view_post/{p_pk}',
            'post': mypost[0]
            }
    return render(request, 'blog/view_posts.html', resp)



# def addMember(request, id):
#     c = Chanel.objects.filter(id=id)
#     c.author.add(request.user)
#     c.save()
#     return render(request, 'blog/channel.html', )
#     # ch = Chanel.objects.filter(id = c)
#     # pass

def addMember(request, id, c):
    u = User.objects.filter(id=id)
    ch = Chanel.objects.filter(id = c)
    pass

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
