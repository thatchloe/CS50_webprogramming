from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post", null=True)
    user = models.CharField(max_length=64)
    content = models.CharField(max_length=64)
    likes = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    



class Like(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liked", null=True)
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="like", null=True)
    

class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following", null=True)
    following_user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers", null=True)
    time = models.DateTimeField(auto_now_add=True)