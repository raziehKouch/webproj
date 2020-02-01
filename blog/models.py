from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




class Chanel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_admin')
    authors = models.ManyToManyField(User, related_name='%(class)s_authors')
    followers = models.ManyToManyField(User, related_name='%(class)s_followers')

    def __str__(self):
        return self.title

class post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE, null=True)
    post_pic = models.ImageField(upload_to='static/blog/image/', null=True, blank=True)

    def __str__(self):
        return self.title
