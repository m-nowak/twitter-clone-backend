import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


class TweetLike(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet",
                              on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class TweetRetweet(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet",
                              on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Tweet(models.Model):
    id = models.BigAutoField(auto_created=True,
                             primary_key=True,
                             editable=False
                             )
    user = models.ForeignKey(User,  related_name='user',
                             on_delete=models.CASCADE)
    text = models.CharField(max_length=200,  null=True,
                            default='', blank=True,)
    photo = models.CharField(max_length=240,  null=True,
                             default='', blank=True, )
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE)
    is_retweet = models.BooleanField(default=False)

    retweets = models.ManyToManyField(
        User, related_name="+", blank=True, through=TweetRetweet)

    likes = models.ManyToManyField(
        User, related_name="+", blank=True, through=TweetLike)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Tweet: " + str(self.id)
