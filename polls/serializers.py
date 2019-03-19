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

    def is_valid(self, raise_exception=False):
        """ check whether 'choice' is owned by 'poll'"""
        ret = super(VoteSerializer, self).is_valid(raise_exception)
        if ret:
            choice = self.validated_data['choice']
            if choice.poll != self.validated_data['poll']:
                errors = self.errors
                msg = "choices: '{}' can only be voted to its owner polls: '{}'"
                errors['non_field_errors'] = [msg.format(
                    choice.choice_text,
                    choice.poll.question
                )]
                if raise_exception:
                    raise ValidationError(errors)
                else:
                    ret = False

        return ret


class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Choice
        fields = "__all__"


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Poll
        fields = "__all__"
