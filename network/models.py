from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    text = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.IntegerField(default=0)
    unlikes = models.IntegerField(default=0)

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id.username,
            "created_at": self.created_at.strftime("%m-%d-%Y, %H:%M %p"),
            "text": self.text,
            "likes": self.likes,
            "unlikes": self.unlikes
        }

class Follow(models.Model):
    c_user = models.OneToOneField(User, primary_key=True,on_delete = models.CASCADE)
    following = models.ManyToManyField(User,related_name='following')
    followers = models.ManyToManyField(User,related_name='followers')

    def user_data(self):
        return{
            "c_user":self.c_user.username,
            "following": [user.id for user in self.following.all()],
            "followers": [user.id for user in self.followers.all()]
        }