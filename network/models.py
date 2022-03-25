from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # id = models.BigAutoField(primary_key=True)
    followers = models.ManyToManyField(
        "self", blank=True, related_name="following", symmetrical=False
    )

    def get_likes_received(self):
        return sum([post.likes.filter(liked=True).count() for post in self.posts.all()])

    def get_likes(self):
        return self.likes.filter(liked=True)

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    content = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def amount_of_likes(self):
        return self.likes.filter(liked=True).count()

    def __str__(self):
        return f"{self.creator} said: {self.content} at {self.created}"


class Like(models.Model):
    liked = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return (
            f"{self.creator} {'liked' if self.liked else 'did not like'} - {self.post}"
        )
