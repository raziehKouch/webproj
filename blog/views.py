import json
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from gym.envs import kwargs
from notifications.signals import notify

from .models import post, Chanel, is_author
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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import render

PAGE = 3

def delete_comment(request, p_pk, c_pk=None):
    # print("cccccccccccccccccccccccccccc",Comment.objects.all() )

    Comment.objects.filter(id=c_pk).delete()
    # print("cccccccccccccccccccccccccccc",Comment.objects.all() )
    # next = request.POST.get('next', f'view_post/{p_pk}')
    return redirect('view_post',p_pk)

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

def home(request):
    # following_post_authors = request.user.profile.get_followers(request.user)
    # print(following_post_authors)
    # following_post_channels =
    # followed = post.objects.filter(author__in = following_post_authors)
    followed_list = post.objects.filter()

    paginator = Paginator(followed_list, PAGE)
    page = request.GET.get('page')
    try:
        followed = paginator.page(page)
    except PageNotAnInteger:
        followed = paginator.page(1)
    except EmptyPage:
        followed = paginator.page(paginator.num_pages)


    time_threshold = timezone.now() - timezone.timedelta(days=7)
    recent_list = post.objects.all().order_by('-date_posted')


    paginator = Paginator(recent_list, PAGE)
    page = request.GET.get('page')
    try:
        recent = paginator.page(page)
    except PageNotAnInteger:
        recent = paginator.page(1)
    except EmptyPage:
        recent = paginator.page(paginator.num_pages)


    hot_list = post.objects.filter(date_posted__gt=time_threshold)#todo.order_('-likes')

    paginator = Paginator(hot_list, PAGE)
    page = request.GET.get('page')
    try:
        hot = paginator.page(page)
    except PageNotAnInteger:
        hot = paginator.page(1)
    except EmptyPage:
        hot = paginator.page(paginator.num_pages)

    contributed_list = post.objects.all()#todo

    paginator = Paginator(contributed_list, PAGE)
    page = request.GET.get('page')
    try:
        contributed = paginator.page(page)
    except PageNotAnInteger:
        contributed = paginator.page(1)
    except EmptyPage:
        contributed = paginator.page(paginator.num_pages)



    context = {
        'followed' : followed,
        'recent' : recent,
        'hot' : hot,
        'contributed' : contributed,
    }
    return render(request, 'blog/home.html', context)


def channel(request):
    clist =  Chanel.objects.all()
    paginator = Paginator(clist, PAGE)
    page = request.GET.get('page')
    try:
        channels = paginator.page(page)
    except PageNotAnInteger:
        channels = paginator.page(1)
    except EmptyPage:
        channels = paginator.page(paginator.num_pages)

    context = {
        'channels':channels
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

def newPostProfile(request,pk):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            ch = form.save(commit=False)
            ch.author = request.user
            c = User.objects.get(id = pk)
            ch.save()
            print("@@@@@@@@@@@@@@@@@@@ before",c,ch.chanel)
            # print("heeeeeeeeeeeeeeeeeeeeeey", f'/profile/{pk}')
            next = request.POST.get('next', f'/profile/{pk}')
            return HttpResponseRedirect(next, messages.success(request, 'post updated.'))

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

def edit_comment(request, c_pk, p_pk):
    mypost = post.objects.filter(id=p_pk)
    c = Comment.objects.filter(id=c_pk)[0]

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
    return render(request, 'blog/comment_thread.html', resp)

def channel_detail(request, id):
    c = Chanel.objects.get(id = id)
    posts_list = post.objects.filter(chanel=c).order_by("-date_posted")

    paginator = Paginator(posts_list,PAGE)
    page = request.GET.get('page')
    try:
        posts= paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
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
    # if pk:

    next = request.POST.get('next','/')
    # print("tttttttttttttttttttttttttttttttttttttttttt",next)



    return HttpResponseRedirect(next,messages.success(request, 'post deleted.'))

    # return #t

def view_post(request, p_pk):
    mypost= post.objects.filter(id = p_pk)
    # ct = ContentType.objects.get_for_model(post)
    # ide = mypost[0].id

    c = Comment.objects.filter_by_instance(mypost[0])

    initial_data={
        "content_type":mypost[0].get_content_type,
        "object_id":mypost[0].id,
    }
    print("KKKKKKKKKKKKKKKKKKKKKKKKK",mypost[0].get_content_type)
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
            notify.send(sender=new_comment.user, recipient=mypost[0].author, verb="new comment!!")
        return redirect('view_post', mypost[0].id)
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







class CommentUpvoteToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Comment, pk=kwargs['p_pk'])
        upvoteurl = obj.get_absolute_url2()
        user = self.request.user
        if user.is_authenticated:
            print('im in first if')
            if user in obj.upvote.all():
                print('im in sec1 if')
                obj.upvote.remove(user)
            else:
                print('im in sec2 if')
                obj.upvote.add(user)
        return upvoteurl


class CommentDownvoteToggle(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Comment, pk=kwargs['id'])
        downvoteurl = obj.get_absolute_url2()
        user = self.request.user
        if user.is_authenticated:
            print('im in first if')
            if user in obj.downvote.all():
                print('im in sec1 if')
                obj.downvote.remove(user)
            else:
                print('im in sec2 if')
                obj.downvote.add(user)
        return downvoteurl



class CommentUpvoteAPI(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, p_pk=None, format=None):
        obj = get_object_or_404(Comment, pk=p_pk)
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.upvote.all():
                liked = False
                obj.upvote.remove(user)
            else:
                liked = True
                obj.upvote.add(user)
            updated = True
        data = {
            'updated': updated,
            'liked': liked,
            'count': obj.upvote.count()
        }
        return Response(data)


class CommentDownvoteToggleAPI(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, p_pk=None, format=None):

        obj = get_object_or_404(Comment, pk=p_pk)
        user = self.request.user
        updated = False
        disliked = False
        if user.is_authenticated:
            if user in obj.downvote.all():
                disliked = False
                obj.downvote.remove(user)
            else:
                disliked = True
                obj.downvote.add(user)
            updated = True
        data = {
            'updated': updated,
            'disliked': disliked,
            'count': obj.downvote.count()
        }
        return Response(data)