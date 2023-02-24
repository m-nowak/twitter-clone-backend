from django.urls import path
from .views import UserView, ListUsersView, MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [

    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', MyTokenRefreshView.as_view(), name='refresh'),
    path('user/', UserView.as_view(), name='load_user'),
    path('users/', ListUsersView.as_view(), name='users'),


]
