from django.db import models
from django.contrib.auth.models import User


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} profile'

    def get_followings(self):
        following_set = follow.objects.filter(follower=self.user)
        return following_set

    def get_followers(self):
        follower_set = follow.objects.filter(following=self.user)
        return follower_set

#follow model
class follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="friend_set", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower} followed {self.following}'


