from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=True, null=True, default='')
    body = models.TextField(blank=True, null=True, default='')
    image = models.FileField(blank=True, null=True)
    post_time = models.DateTimeField(auto_now=True)
    
class PostComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    comment_body = models.TextField(max_length=256, blank=True, default='')
    comment_time = models.DateTimeField(auto_now=True)
    
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
    
class PostDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')

class UserFollow(models.Model):
    id = models.BigAutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')    
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    created_at = models.DateTimeField(auto_now_add=True)    