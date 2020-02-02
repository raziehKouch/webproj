from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum

from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Replace models. Model with MPTT Model
class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        ct = ContentType.objects.get_for_model(instance.__class__)
        ide = instance.id
        qs = super(CommentManager,self).filter(content_type=ct, object_id=ide)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    objects = CommentManager()
    class Meta:
        ordering = ['-timestamp']
    def children(self):#replies
        return Comment.objects.filter(parent = self)
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Chanel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_admin')
    authors = models.ManyToManyField(User, related_name='%(class)s_authors')
    followers = models.ManyToManyField(User, related_name='%(class)s_followers')

    def get_followers(self):
        follower_set = subscribe.objects.filter(following_channel=self)
        return follower_set


class post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE, null=True, blank= True)
    post_pic = models.ImageField(upload_to='post_picd', null=True, blank=True)

    @property
    def comments(self):
        qs = Comment.objects.filter_by_instance(self)
        return qs

    @property
    def get_content_type(self):
        ct = ContentType.objects.get_for_model(self.__class__)
        return ct


class subscribe(models.Model):
        subscriber = models.ForeignKey(User, related_name="subscriber", on_delete=models.CASCADE)
        following_channel = models.ForeignKey(Chanel, related_name="friend_set", on_delete=models.CASCADE)
        def __str__(self):
            return f'{self.follower} followed {self.following}'

class Like(models.Model):
        post = models.ForeignKey(post, on_delete=models.CASCADE)
