# views.py
from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer


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
            )
        return UserProfile.objects.none()
