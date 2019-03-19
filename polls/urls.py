from django.conf.urls import url
from . import apiviews

urlpatterns = [
    url(r'^polls/$', apiviews.PollList.as_view(), name='polls_list'),
    url(r'^polls/(?P<pk>\d+)', apiviews.PollDetail.as_view(), name='polls_detail'),

]
