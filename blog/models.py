from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum
from tinymce.models import HTMLField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Replace models. Model with MPTT Model
class CommentManager(models.Manager):
    def all(self):
        qs=super(CommentManager,self).filter(parent= None)
        return qs
    def filter_by_instance(self, instance):
        ct = ContentType.objects.get_for_model(instance.__class__)
        ide = instance.id
        qs = super(CommentManager,self).filter(content_type=ct, object_id=ide).filter(parent=None)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    upvote = models.ManyToManyField(User, blank=True, related_name="comment_upvote")
    downvote = models.ManyToManyField(User, blank=True, related_name="comment_downvote")
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
    def get_absolute_url(self):
        return reverse("comment_thread", kwargs={"id":self.id, })

    def get_absolute_url2(self):
        return reverse("view_post", kwargs={"p_pk":self.object_id, })

    def get_upvote_url(self):
        return reverse('upvote', kwargs={'id': self.pk})

    def get_downvote_url(self):
        return reverse('downvote', kwargs={'id': self.pk})

    def get_downvote_api_url(self):
        return reverse('downvote-api', kwargs={'id': self.pk})

    def get_upvote_api_url(self):
        return reverse('upvote-api', kwargs={'id': self.pk})



class Chanel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_admin')
    # authors = models.ManyToManyField(User, related_name='%(class)s_authors')
    followers = models.ManyToManyField(User, related_name='%(class)s_followers')
    timestamp = models.DateTimeField(default=timezone.now)

    def get_channel_auths(self):
        author_set = is_author.objects.filter(channel=self)
        # author_set |= User.objects.filter(id = self.admin.id)
        return author_set

    def get_followers(self):
        follower_set = subscribe.objects.filter(following_channel=self)
        return follower_set
    class Meta:
        ordering = ["-timestamp"]

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



class is_author(models.Model):
    author = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)
    channel = models.ForeignKey(Chanel, related_name="auth_channel", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} is author of {self.channel.title}'
