from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from .models import Poll, Choice, Vote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        extra_kwargs = {
            'voted_by': {'required': False},
            'poll': {'required': False},
            'choice': {'required': False}
        }


class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Choice
        fields = "__all__"
        extra_kwargs = {
            'poll': {'required': False}
        }


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Poll
        fields = "__all__"
        extra_kwargs = {'created_by': {'read_only': True}}
        depth = 1
