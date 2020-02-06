from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import is_author, is_member, Comment


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # def __str__(self):
    #     return f'{self.user.username} profile'

    def get_followings(self):
        following_set = follow.objects.filter(follower=self.user).values('following')
        return following_set

    def get_followers(self):
        follower_set = follow.objects.filter(following=self.user).values('follower')
        return follower_set

    def get_comments(self):
        return Comment.objects.filter(user=self.user)

    def get_auth_channels(self):
        return is_author.objects.filter(author=self.user).values('channel')

    def get_following_channels(self):
        return is_member.objects.filter(member=self.user).values('channel')

    def follow_user(self, ruser):
        if follow.objects.filter(following=self.user, follower = ruser).count() == 0:
            follow.objects.create(follower = ruser, following=self.user)
        else:
            follow.objects.filter(follower=ruser, following=self.user).delete()

    def get_follower_id(self):
        return follow.objects.filter(following=self.user).values_list('follower_id', flat=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'p_pk': self.user.pk})

    def get_follow_url(self):
        return reverse('follow', kwargs={'p_pk': self.user.pk})


class follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="friend_set", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower} followed {self.following}'


