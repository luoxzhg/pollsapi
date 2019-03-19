from django.conf.urls import url
from . import apiviews

urlpatterns = [
    url(r'^polls/$', apiviews.PollList.as_view(), name='poll_list'),
    url(r'^polls/(?P<pk>\d+)', apiviews.PollDetail.as_view(), name='poll_detail'),
    url(r'^choices/$', apiviews.ChoiceList.as_view(), name='choice_list'),
    url(r'^vote/$', apiviews.CreateVote.as_view(), name='create_vote'),

]
