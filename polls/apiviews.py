from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Poll, Choice
from .serializers import (UserSerializer,
                          PollSerializer,
                          ChoiceSerializer,
                          VoteSerializer)


# Create your views here.
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return Choice.objects.filter(poll=self.kwargs['poll_pk'])


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer(self, *args, **kwargs):
        data = kwargs.get('data', None)
        if data:
            data = data.copy()
            data.setdefault('poll', self.kwargs['poll_pk'])
            data.setdefault('choice', self.kwargs['choice_pk'])
            data.setdefault('voted_by', self.request.user.pk)
            kwargs['data'] = data
        return super(CreateVote, self).get_serializer(*args, **kwargs)


class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user:
            token = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'wrong credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
