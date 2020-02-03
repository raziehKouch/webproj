from django.db import models
from django.urls import reverse
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
    # authors = models.ManyToManyField(User, related_name='%(class)s_authors')
    followers = models.ManyToManyField(User, related_name='%(class)s_followers')

    def get_channel_auths(self):
        author_set = is_author.objects.filter(channel=self)
        # author_set |= User.objects.filter(id = self.admin.id)
        return author_set

class post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE, null=True, blank= True)
    post_pic = models.ImageField(upload_to='post_picd', null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    def get_absolute_url(self):
        return reverse('view_post', kwargs={'p_pk': self.pk})

    def get_like_url(self):
        return reverse('like', kwargs={'p_pk': self.pk})

    def get_like_api_url(self):
        return reverse('like-api', kwargs={'p_pk': self.pk})



class Comment(models.Model):
    content = models.TextField()
    comment_pic = models.ImageField(upload_to='comment_picd', null=True, blank=True)



class is_author(models.Model):
    author = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)
    channel = models.ForeignKey(Chanel, related_name="auth_channel", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} is author of {self.channel.title}'
