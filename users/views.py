from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import profile
from django.contrib.auth.models import User

def view_profile(request, p_pk):
    myuser = User.objects.get(id = p_pk)
    resp = {'shared_url' : f'127.0.0.1/view_profile/{p_pk}',
            'user': myuser
            }
    return render(request, 'users/view_profile.html', resp)


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
def xprofile(request):
    return render(request, 'users/profile.html')
