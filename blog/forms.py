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
        fields = ('title', 'content', 'post_pic')
        exclude = ['chanel']

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)