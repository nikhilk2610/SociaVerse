# views.py
from django.db.models import Q
# from django.utils.decorators import method_decorator
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
# from ratelimit.decorators import ratelimit

from .models import UserProfile, FriendRequest, RequestStatus
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer, FriendRequestSerializer
from .throttling import FriendRequestThrottle


class UserSignupView(APIView):

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)


class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_keyword = self.request.query_params.get('query')
        if search_keyword:
            return UserProfile.objects.filter(
                Q(name__icontains=search_keyword) | Q(email__iexact=search_keyword)
            ).order_by("name")
        return UserProfile.objects.none()


class FriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def create(self, request, *args, **kwargs):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        if not receiver_id:
            return Response({'error': 'Receiver id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = UserProfile.objects.get(pk=receiver_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Receiver does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if sender == receiver:
            return Response({'error': 'You cannot send a friend request to yourself'},
                            status=status.HTTP_400_BAD_REQUEST)

        already_exists = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
        if already_exists:
            return Response({'error': 'A friend request has already been sent to this user'},
                            status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendRequestActionAPIView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        sender_id = request.data.get('sender_id')
        action = request.data.get('action')
        if not action or action not in ('accept', 'reject'):
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = get_object_or_404(FriendRequest, pk=sender_id)

        if action == 'accept':
            friend_request.status = RequestStatus.ACCEPTED.value
        elif action == 'reject':
            friend_request.status = RequestStatus.REJECTED.value

        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data)


class FriendsListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(sender=user, status='accepted').order_by('-created_at').values_list('receiver')
        return UserProfile.objects.filter(pk__in=friends)


class FriendRequestsListAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(receiver=user, status='pending').order_by('-created_at')
