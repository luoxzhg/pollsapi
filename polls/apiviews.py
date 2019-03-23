from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Poll, Choice
from .permissions import IsOwnerOrReadOnly
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
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Choice.objects.filter(poll=self.kwargs['poll_pk'])

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['poll'] = kwargs['poll_pk']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if request.user != serializer.validated_data['poll'].created_by:
            raise permissions.PermissionDenied(
                "Only the owner of the poll can create choice."
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, poll_pk, choice_pk):
        data = request.data.copy()
        data.update({
            'poll': int(poll_pk),
            'choice': int(choice_pk),
            'voted_by': request.user.pk
        })
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
