from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from tweets.permisions import IsOwnerUser
from tweets.models import Tweet, TweetLike, TweetRetweet
from tweets.serializers import TweetSerializer, TweetCountSerializer, TweetListSerializer, TweetCreateSerializer, TweetLikeSerializer, TweetRetweetSerializer
from tweets.paginations import PagePagination
from django.db.models import Count


class TweetListView(generics.ListAPIView):
    # permission_classes = (AllowAny,)
    queryset = Tweet.objects.filter(parent=None).order_by("-created_at")
    serializer_class = TweetListSerializer
    pagination_class = PagePagination


class TweetCountView(generics.ListAPIView):

    # permission_classes = (AllowAny,)
    queryset = Tweet.objects.filter(parent=None).values(
        'user_id').annotate(count=Count('user_id'))
    serializer_class = TweetCountSerializer


class TweetCreateView(generics.CreateAPIView):
    # permission_classes = (AllowAny,)
    queryset = Tweet.objects.all().first()
    serializer_class = TweetCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwnerUser,)
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class TweetLikeView(generics.CreateAPIView):
    # permission_classes = (AllowAny,)
    serializer_class = TweetLikeSerializer

    def perform_create(self, serializer):

        try:

            pk = self.kwargs.get('pk')
            tweet = Tweet.objects.get(pk=pk)
            # user = self.request.data['user']
            user = self.request.user
            like = TweetLike.objects.filter(
                tweet=tweet, user=user)
            if like.exists():
                like.delete()
            else:
                serializer.save(user=user, tweet=tweet)
        except:
            return Response(
                {'error': 'Something went wrong with like or unlike'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TweetRetweetView(generics.CreateAPIView):
    # permission_classes = (AllowAny,)
    serializer_class = TweetRetweetSerializer

    def perform_create(self, serializer):
        try:
            pk = self.kwargs.get('pk')
            tweet = Tweet.objects.get(pk=pk)
            user = self.request.user
            retweet = TweetRetweet.objects.filter(tweet=tweet, user=user)
            if retweet.exists():
                tweet = Tweet.objects.filter(
                    parent=tweet, user=user, is_retweet=True)
                retweet.delete()
                tweet.delete()
            else:
                serializer.save(user=user, tweet=tweet)
        except:
            return Response(
                {'error': 'Something went wrong with retweet'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TweetDetailView(generics.RetrieveAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetListSerializer


class ReplyListView(generics.ListAPIView):
    serializer_class = TweetListSerializer
    pagination_class = PagePagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Tweet.objects.filter(parent=pk).order_by("-created_at")
