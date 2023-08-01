from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchAPIView, FriendRequestAPIView, FriendRequestActionAPIView, \
    FriendsListAPIView, PendingFriendRequestsListAPIView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-requests/', FriendRequestAPIView.as_view(), name='friend-request'),
    path('friend-requests/action/', FriendRequestActionAPIView.as_view(), name='friend-request-action'),
    path('friends/', FriendsListAPIView.as_view(), name='friends-list'),
    path('pending-friend-requests/', PendingFriendRequestsListAPIView.as_view(), name='pending-friend-requests-list'),
]
