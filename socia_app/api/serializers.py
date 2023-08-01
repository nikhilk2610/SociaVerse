from rest_framework import serializers
from .models import UserProfile, FriendRequest
from django.contrib.auth import authenticate


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        email = UserProfile.objects.normalize_email(validated_data['email'])
        name = validated_data['name']
        password = validated_data['password']

        user = UserProfile.objects.create_user(email=email, username=email, password=password, name=name)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'].lower(), password=data['password'])
        if user:
            if user.is_active:
                data['user'] = user
            else:
                raise serializers.ValidationError("User account is inactive.")
        else:
            raise serializers.ValidationError("Invalid credentials. Try again with correct credentials.")
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'name']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['sender', 'receiver', 'status', 'created_at']
