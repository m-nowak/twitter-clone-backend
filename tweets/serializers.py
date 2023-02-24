# import json
from rest_framework import serializers
# from django.http import JsonResponse, HttpResponse
from tweets.models import Tweet, TweetLike, TweetRetweet
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_photo')


class TweetLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TweetLike
        # fields = "__all__"
        exclude = ('tweet',)


class TweetRetweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TweetRetweet
        # fields = "__all__"
        exclude = ('tweet',)

    def create(self, validated_data):
        user = validated_data['user']
        tweet = validated_data['tweet']
        is_retweet = True
        retweet = TweetRetweet.objects.create(**validated_data)
        Tweet.objects.create(user=user, parent=tweet, is_retweet=is_retweet)
        return retweet


class TweetSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    retweets_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = "__all__"

    def get_replies_count(self, obj):
        replies = Tweet.objects.filter(parent=obj.id, is_retweet=False).count()
        return replies

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_retweets_count(self, obj):
        return obj.retweets.count()


class TweetListSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    parent = TweetSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    retweets_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = "__all__"

    def get_replies_count(self, obj):
        replies = Tweet.objects.filter(parent=obj.id, is_retweet=False).count()
        return replies

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_retweets_count(self, obj):
        return obj.retweets.count()


class TweetCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = "__all__"

    # def validate_text(self, value):
    #     if len(value) < 2 and len(value) < 0:
    #         raise serializers.ValidationError("Text is too short!")
    #     else:
    #         return value


class TweetCountSerializer(serializers.ModelSerializer):

    # user = UserSerializer(read_only=True)
    count = serializers.IntegerField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['user', 'count']

    def get_user(self, obj):
        user = User.objects.filter(id=obj['user_id']).first()
        return user.first_name + ' ' + user.last_name
