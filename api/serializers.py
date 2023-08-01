from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import authenticate


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email', 'password')

    def create(self, validated_data):
        email = UserProfile.objects.normalize_email(validated_data['email'])
        password = validated_data['password']

        # Create the user with normalized email
        user = UserProfile.objects.create_user(email=email, username=email, password=password)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'].lower(), password=data['password'])
        print(data)
        print(user)
        if user:
            if user.is_active:
                data['user'] = user
            else:
                raise serializers.ValidationError("User account is inactive.")
        else:
            raise serializers.ValidationError("Invalid credentials. Try again with correct credentials.")
        return data
