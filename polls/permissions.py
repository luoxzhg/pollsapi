from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Choice


class IsOwnerOrReadOnly(BasePermission):
    """
    custom permission to only allow the owner of a object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user == obj.created_by


class IsOwnerOfPoll(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.poll.created_by


class IsPollOwnChoice(BasePermission):
    message = 'Choice can only be voted to its owner poll'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        choice = Choice.objects.get(pk=int(request.resolver_match.kwargs['choice_pk']))
        return choice.poll.pk == int(request.resolver_match.kwargs['poll_pk'])
