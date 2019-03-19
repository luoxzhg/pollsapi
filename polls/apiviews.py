from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer


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

