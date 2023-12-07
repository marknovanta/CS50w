from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.CharField(max_length=64)
    content = models.CharField(max_length=140)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "timestamp": self.timestamp,
            "content": self.content,
            "likes": self.likes
        }



class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Follower')
    follows = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='Following')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Who_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Post_liked")