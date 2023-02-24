from django.contrib import admin
from tweets.models import Tweet, TweetLike, TweetRetweet

admin.site.register(Tweet)
admin.site.register(TweetLike)
admin.site.register(TweetRetweet)
