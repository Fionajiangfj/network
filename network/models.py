from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)


class Post(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    
    
class Like(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)