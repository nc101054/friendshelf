from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Post(models.Model):
    KINDS = [
        ("book", "书"),
        ("movie", "电影"),
        ("podcast", "播客"),
          ("other", "其他"),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    kind = models.CharField(max_length=10, choices=KINDS)
    title = models.CharField(max_length=200)
    thoughts = models.TextField()
    is_public = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_kind_display()} {self.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
