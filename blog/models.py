from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum



class Chanel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_admin')
    authors = models.ManyToManyField(User, related_name='%(class)s_authors')
    followers = models.ManyToManyField(User, related_name='%(class)s_followers')

class post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE, null=True)
    post_pic = models.ImageField(upload_to='post_picd', null=True, blank=True)



class Comment(models.Model):
    content = models.TextField()
    comment_pic = models.ImageField(upload_to='comment_picd', null=True, blank=True)

class Like(models.Model):
        post = models.ForeignKey(post, on_delete=models.CASCADE)
