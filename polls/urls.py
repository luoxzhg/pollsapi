from django.conf.urls import url

from rest_framework.routers import DefaultRouter
from . import apiviews


router = DefaultRouter()
router.register('polls', apiviews.PollViewSet, base_name='polls')


urlpatterns = [
    url(r'^polls/(?P<poll_pk>\d+)/choices/$',
        apiviews.ChoiceList.as_view(), name='choice_list'),

    url(r'^polls/(?P<poll_pk>\d+)/choices/(?P<choice_pk>\d+)/vote/$',
        apiviews.CreateVote.as_view(), name='create_vote'),

    url(r'^users/$', apiviews.CreateUser.as_view(), name='create_user'),

    url(r'^login/$', apiviews.LoginView.as_view(), name='login'),
]

urlpatterns += router.urls

