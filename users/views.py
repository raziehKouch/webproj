from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import RedirectView

from .forms import UserRegisterForm, UserUpdateForm, profileupdateform
from django.contrib.auth.decorators import login_required
# from .models import profile
from django.contrib.auth.models import User
from blog.models import post



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! you are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def editprofile(request):
    following_count = request.user.profile.get_followings().count()
    follower_count = request.user.profile.get_followers().count()
    post_count = post.objects.filter(author = request.user ).count()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST ,instance=request.user)
        p_form = profileupdateform(request.POST ,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            context = {
                'following_count': following_count,
                'follower_count': follower_count,
                'post_count': post_count,
            }
            return redirect('profile', context)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = profileupdateform(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'following_count' : following_count,
        'follower_count' : follower_count,
        'post_count': post_count,
    }
    return render(request, 'users/profile_edit.html', context)

def profile(request, p_pk):
    ruser = User.objects.get(pk = p_pk)
    following_count = ruser.profile.get_followings().count()
    follower_count = ruser.profile.get_followers().count()
    post_count = post.objects.filter(author=ruser).count()
    posts = post.objects.filter(author=ruser)
    context = {
        'requested_user': ruser,
        'following_count' : following_count,
        'follower_count' : follower_count,
        'post_count': post_count,
        'posts' : posts
    }
    return render(request, 'users/profile.html', context)


class FollowToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(User, pk=kwargs['p_pk'])
        followurl = obj.profile.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            obj.profile.follow_user(user)
        return followurl


