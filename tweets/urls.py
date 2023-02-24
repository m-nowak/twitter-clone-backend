from django.urls import path
from tweets.views import TweetListView, TweetCountView, TweetCreateView, TweetDeleteView, TweetLikeView, TweetRetweetView, TweetDetailView, ReplyListView


urlpatterns = [

    path('list/', TweetListView.as_view(), name='tweet-list'),
    path('count/', TweetCountView.as_view(), name='tweet-count'),
    path('create/', TweetCreateView.as_view(), name='tweet-create'),
    path('<int:pk>/like/', TweetLikeView.as_view(), name='tweet-like'),
    path('<int:pk>/retweet/', TweetRetweetView.as_view(), name='tweet-retweet'),
    path('<int:pk>/delete/', TweetDeleteView.as_view(), name='tweet-delete'),
    path('<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('<int:pk>/replies/', ReplyListView.as_view(), name='replies-list'),

]
