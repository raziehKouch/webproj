from django import forms
from django.contrib.auth.models import User

from .models import Chanel, post


class channelForm(forms.ModelForm):

    class Meta:
        model = Chanel
        fields = ('title', 'description', 'rules')



class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('title', 'content')

