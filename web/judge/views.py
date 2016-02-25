from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from django.db.models import Max
from django.contrib.auth.models import User
from .models import Problem

from django.contrib.auth import views as auth_views

from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileUpdateBitbucketForm

def index(request):
    return render(request, 'judge/index.html')

def login(request):
    # users should not be able to log in again if there're already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('judge:index'))
    else:
        return auth_views.login(request, template_name='judge/login.html')

def logout(request):
    # users should not be able to log out if there're not already logged in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('judge:index'))
    else:
        return auth_views.logout(request, next_page='judge:index')

def problem_list(request):
    profile = request.user.profile

    problem_list = Problem.objects.all()
    profile_hiscore_list = []
    for problem in problem_list:
        profile_submission_list = problem.submission_set.filter(profile=profile)
        profile_hiscore_list.append(profile_submission_list.aggregate(Max('score'))['score__max'])
    problem_profile_hiscore_list = zip(problem_list, profile_hiscore_list)

    return render(request,
                  'judge/problem_list.html',
                  {'problem_profile_hiscore_list': problem_profile_hiscore_list})

def problem_detail(request, pk):
    profile = request.user.profile

    problem = get_object_or_404(Problem, pk=pk)
    profile_submission_list = problem.submission_set.filter(profile=profile)
    profile_hiscore = profile_submission_list.aggregate(Max('score'))['score__max']

    return render(request,
                  'judge/problem_detail.html',
                  {'problem': problem,
                   'profile_submission_list': profile_submission_list,
                   'profile_hiscore': profile_hiscore})

def profile(request):
    user = request.user
    profile = user.profile

    # unbound forms to be used later
    unbound_update_bitbucket_form = ProfileUpdateBitbucketForm(instance=profile,
                                                               initial={'bitbucket_account':
                                                                        profile.bitbucket_account,
                                                                        'bitbucket_repository':
                                                                        profile.bitbucket_repository})
    unbound_password_change_form = PasswordChangeForm(user=user)

    # handle forms
    if request.method == 'POST':
        update_bitbucket_form = ProfileUpdateBitbucketForm(data=request.POST,
                                                           instance=profile,
                                                           initial={'bitbucket_account':
                                                                    profile.bitbucket_account,
                                                                    'bitbucket_repository':
                                                                    profile.bitbucket_repository})
        password_change_form = PasswordChangeForm(data=request.POST, user=user)

        # for it to be regarded as successful (such that the user gets
        # redirected back to profile), all changed forms must be valid and saved
        # already; otherwise, render the view with all forms again (with
        # unchanged ones replaced by unbound ones, so as to clean their errors),
        # in order for the user to know what errors have occurred
        n_undone_forms = update_bitbucket_form.has_changed() + password_change_form.has_changed()

        if update_bitbucket_form.has_changed():
            if update_bitbucket_form.is_valid():
                update_bitbucket_form.save()
                n_undone_forms -= 1

                messages.success(request,
                                'Bitbucket settings successfully updated.')
        else:
            update_bitbucket_form = unbound_update_bitbucket_form

        if password_change_form.has_changed():
            if password_change_form.is_valid():
                password_change_form.save()
                n_undone_forms -= 1

                messages.success(request,
                                'Password successfully changed. Please log in again.')
        else:
            password_change_form = unbound_password_change_form

        if n_undone_forms == 0:
            return HttpResponseRedirect(reverse('judge:profile'))
    else:
        update_bitbucket_form = unbound_update_bitbucket_form
        password_change_form = unbound_password_change_form

    return render(request,
                  'judge/profile.html',
                  {'profile': profile,
                   'update_bitbucket_form': update_bitbucket_form,
                   'password_change_form': password_change_form})
