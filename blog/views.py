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
        form = PostForm(request.POST)
        if form.is_valid():
            ch = form.save(commit=False)
            ch.author = request.user
            ch.chanel = Chanel.objects.get(id= pk)
            ch.save()

            return HttpResponseRedirect('viewPosts', messages.success(request, 'Channel created.'))
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


def viewPosts(request, pk):
    try:
        selected_posts = post.objects.get(chanel__id= pk)
        context = {
                'posts': selected_posts,
                'pk_ch': pk
            }
        return render(request, 'blog/channel_posts.html', context)
    except:
        context = {
            'pk_ch': pk
        }
        return render(request, 'blog/channel_posts.html', context)

def delete_channel(request, id):
    Chanel.objects.filter(id=id).delete()
    next = request.POST.get('next', '/channels')
    return HttpResponseRedirect(next)

def addMember(request, id, c):
    u = User.objects.filter(id=id)
    ch = Chanel.objects.filter(id = c)
    pass

