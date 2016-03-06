from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'judge'
urlpatterns = [
    url(r'^$',
        login_required(views.index),
        name='index'),

    url(r'^login/$',
        views.login,
        name='login'),

    url(r'^logout/$',
        views.logout,
        name='logout'),

    url(r'^problems/$',
        login_required(views.problem_list),
        name='problem_list'),

    url(r'^problems/(?P<pk>\d+)/$',
        login_required(views.problem_detail),
        name='problem_detail'),

    url(r'^profile/$',
        login_required(views.profile),
        name='profile'),

    url(r'^submissions/(?P<pk>\d+)/$',
        login_required(views.submission_detail),
        name='submission_detail'),
]
