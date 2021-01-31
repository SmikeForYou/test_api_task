from typing import Union
from django.db import models
from django.contrib.auth import get_user_model
from core import mixins as core_mixins

user_model = get_user_model()

class Post(core_mixins.DateAddedMixin):
    title = models.CharField(max_length=128)
    body = models.TextField()
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)

    def liked_by_user(self, user):
        like, _ = self.postlikes_set.get_or_create(user=user)
        return like.liked

    def set_liked_status(self, user, liked: bool):
        if liked is not None:
            like, _ = self.postlikes_set.get_or_create(user=user)
            like.liked = liked
            like.save()




class PostLikes(core_mixins.DateAddedMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)