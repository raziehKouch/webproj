from django.db import models
from django.urls import reverse
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

class Chanel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_admin')
    # authors = models.ManyToManyField(User, related_name='%(class)s_authors')
    # followers = models.ManyToManyField(User, related_name='%(class)s_followers')

    def get_channel_auths(self):
        return is_author.objects.filter(channel=self).values('author')

    def get_channel_auths_id(self):
        return is_author.objects.filter(channel=self).values_list('author', flat=True)

    def get_channel_members(self):
        return is_member.objects.filter(channel=self).values('member')

    def get_channel_members_id(self):
        return is_member.objects.filter(channel=self).values_list('member', flat=True)

    def follow_channel_url(self):
        return reverse('followChannel', kwargs={'chID':self.pk})

    def add_author_url(self, uID):
        return reverse('addAuthorNow', kwargs={'chID':self.pk, 'uID':uID})

    def get_absolute_url(self):
        return reverse('channel_detail', kwargs={'id': self.pk})

    def follow_channel(self, user):
        member = user
        if is_member.objects.filter(member=member, channel=self).count() == 0:
            is_member.objects.create(member=member, channel=self)
        else:
            is_member.objects.filter(member=member, channel=self).delete()

    def addAuthorNow(self, user):
        auth = user,
        if is_author.objects.filter(author=auth, channel=self).count() == 0:
            is_author.objects.create(author=auth, channel=self)
        else:
            is_author.objects.filter(author=auth, channel=self).delete()


class post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE, null=True, blank= True)
    post_pic = models.ImageField(upload_to='post_picd', null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='post_dislikes')

    def get_absolute_url(self):
        return reverse('view_post', kwargs={'p_pk': self.pk})

    def get_like_url(self):
        return reverse('like', kwargs={'p_pk': self.pk})

    def get_dislike_url(self):
        return reverse('dislike', kwargs={'p_pk': self.pk})

    def get_dislike_api_url(self):
        return reverse('dislike-api', kwargs={'p_pk': self.pk})

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


class is_member(models.Model):
    member = models.ForeignKey(User, related_name="member", on_delete=models.CASCADE)
    channel = models.ForeignKey(Chanel, related_name="mem_channel", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.member} is a member of {self.channel.title}'
