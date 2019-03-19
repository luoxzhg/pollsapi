from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Poll, Choice
from .permissions import (IsOwnerOrReadOnly,
                          IsOwnerOfPoll,
                          IsPollOwnChoice)
from .serializers import (UserSerializer,
                          PollSerializer,
                          ChoiceSerializer,
                          VoteSerializer)


# Create your views here.
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOfPoll)

    def get_queryset(self):
        return Choice.objects.filter(poll=self.kwargs['poll_pk'])

    def create(self, request, *args, **kwargs):
        request.data['poll'] = kwargs['poll_pk']
        return super(ChoiceList, self).create(request, *args, **kwargs)


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsPollOwnChoice)

    def create(self, request, poll_pk, choice_pk):
        request.data.update({
            'poll': int(poll_pk),
            'choice': int(choice_pk),
            'voted_by': request.user.pk
        })
        return super().create(request)


class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'wrong credentials'},
                            status=status.HTTP_400_BAD_REQUEST)
