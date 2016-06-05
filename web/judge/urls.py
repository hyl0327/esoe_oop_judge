from django.conf.urls import url

from . import views


app_name = 'judge'

urlpatterns = [
    url(r'^$',
        views.index,
        name='index'),

    url(r'^login/$',
        views.login,
        name='login'),

    url(r'^logout/$',
        views.logout,
        name='logout'),

    url(r'^problems/$',
        views.problem_list,
        name='problem_list'),

    url(r'^problems/(?P<pk>\d+)/$',
        views.problem_detail,
        name='problem_detail'),

    url(r'^profile/$',
        views.profile,
        name='profile'),

    url(r'^submissions/(?P<pk>\d+)/$',
        views.submission_detail,
        name='submission_detail'),
]
