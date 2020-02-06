import json
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import post, Chanel, is_author, is_member
from .forms import channelForm, PostForm, CommentForm
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
from .models import Comment
from django.db.models import Count


def comment_thread(request,id):
    obj = get_object_or_404(Comment, id=id)
    content_object = obj.content_object
    content_id = obj.content_object.id
    initial_data={
        "content_type":obj.content_type,
        "object_id":obj.object_id,
    }
    print("kkkkkkkkkkkkkkkkkk",obj.id)
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        print("valiiiiiiiiiiiiiiiiid")
        c_type = form.cleaned_data.get("content_type")
        object_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        try:
            print("heeeeeeeeeeeeeeeelo")
            parent_id = int(request.POST.get("parent_id"))
        except:
            print("byeeeeeeeeeeeeee")
            parent_id = None
        parent_obj = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        content_type = ContentType.objects.get(model=c_type)
        new_comment, created = Comment.objects.get_or_create(user=request.user, content_type=content_type,
                                                             object_id=object_id, content=content_data,
                                                             parent=parent_obj)
        if created:
            print("workedddddddddddddddddd" , obj.id)
        return redirect('comment_thread', obj.id)
    context = {'comment':obj,
               'form':form
               }
    return render(request, 'blog/comment_thread.html',context   )

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
    following_post_authors = request.user.profile.get_followings()
    following_post_channels = request.user.profile.get_following_channels() #todo: add posts with the channel we are following (notice: beware of duplicates)
    followed = post.objects.filter(author__in = following_post_authors) | post.objects.filter(chanel__in = following_post_channels)
    time_threshold = timezone.now() - timezone.timedelta(days=7)
    recent = post.objects.all().order_by('-date_posted')
    hot = post.objects.filter(date_posted__gt=time_threshold).annotate(like_count = Count('likes')).order_by('-like_count')
    contributed = post.objects.filter(author=request.user)#todo commented on
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
            ch.chanel = c
            ch.save()
            return HttpResponseRedirect('channel_detail', messages.success(request, 'Post created.'))#todo
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
    # ct = ContentType.objects.get_for_model(post)
    # ide = mypost[0].id

    c = Comment.objects.filter_by_instance(mypost[0])

    initial_data={
        "content_type":mypost[0].get_content_type,
        "object_id":mypost[0].id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    resp = {'shared_url' : f'127.0.0.1/view_post/{p_pk}',
            'post': mypost[0],
            'comments': c,
            'form': form,
            }
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        object_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        parent_obj=None
        if parent_id:
            parent_qs = Comment.objects.filter(id= parent_id)
            if parent_qs.exists() :
                parent_obj=parent_qs.first()
        content_type = ContentType.objects.get(model = c_type)
        new_comment , created = Comment.objects.get_or_create(user = request.user, content_type = content_type, object_id=object_id, content = content_data, parent=parent_obj )
        if created:
            print("worked")
        return redirect('view_post', mypost[0].id)
    return render(request, 'blog/view_posts.html', resp)

def subAuthor(request, id):
    context = {
        'channel' : Chanel.objects.get(id = id),
    }
    return render(request, 'blog/subAuthor.html', context )


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

class FollowChannelToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Chanel, pk=kwargs['chID'])
        followurl = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            obj.follow_channel(user)
        return followurl

class AddAuthorToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Chanel, pk=kwargs['chID'])
        url = obj.get_absolute_url()
        user = get_object_or_404(User, pk=kwargs['uID'])
        # todo: if self.request.user.is_channelAdmin:
        obj.addAuthorNow(user)
        return url

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


class postDisliketoggle(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(post, pk=kwargs['p_pk'])
        dislikeurl = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            print('im in first if')
            if user in obj.dislikes.all():
                print('im in sec1 if')
                obj.dislikes.remove(user)
            else:
                print('im in sec2 if')
                obj.dislikes.add(user)
        return dislikeurl



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


class PostDisLikeToggleAPI(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, p_pk=None, format=None):

        obj = get_object_or_404(post, pk=p_pk)
        user = self.request.user
        updated = False
        disliked = False
        if user.is_authenticated:
            if user in obj.dislikes.all():
                disliked = False
                obj.dislikes.remove(user)
            else:
                disliked = True
                obj.dislikes.add(user)
            updated = True
        data = {
            'updated': updated,
            'disliked': disliked,
            'count': obj.dislikes.count()
        }
        return Response(data)