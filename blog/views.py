from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import post, Chanel
from .forms import channelForm, PostForm
from django.contrib import messages
def home(request):
    context = {
        'posts': post.objects.all()
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

            return HttpResponseRedirect('viewPosts', messages.success(request, 'Post created.'))
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


def viewPosts(request, pk):
    user = Chanel.objects.only('id').get(id=pk)
    posts = post.objects.filter ( chanel=user)
    print("rrrrrrrrrrrrr", posts)

    # c = Chanel.objects.filter(pk = pk)
    # print(c__id)
    # posts = post.objects.filter(chanel = c)
    cX = {
        'posts':posts,
         'ch_pk':pk,
    }
    return render(request, 'blog/channel_posts.html', cX)


def delete_channel(request, id):
    Chanel.objects.filter(id=id).delete()
    next = request.POST.get('next', '/channels')
    return HttpResponseRedirect(next)

def addMember(request, id, c):
    u = User.objects.filter(id=id)
    ch = Chanel.objects.filter(id = c)
    pass

