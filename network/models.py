from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    def __str__(self):
        return f"{self.username} {self.email}"


class Post(models.Model):
    content = models.TextField(max_length=500)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post id {self.pk} by {self.user.username}"

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.user.username,
            "creator_id": self.user.id,
            "content": self.content,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
