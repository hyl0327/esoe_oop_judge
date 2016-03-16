import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from django.db.models import Max
from django.contrib.auth.models import User
from .models import Problem, Submission

from django.contrib.auth import views as auth_views

from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileUpdateBitbucketForm

def index(request):
    sample_problem = Problem.objects.get(pk=config.WEB_INDEX_SAMPLE_PROBLEM_ID)

    return render(request,
                  'judge/index.html',
                  {'bitbucket_account': config.BITBUCKET_ACCOUNT,
                   'sample_problem': sample_problem})

def login(request):
    # users should not be able to log in again if they're already logged in
    if request.user.is_authenticated():
        messages.error(request,
                       'You are already logged in.')
        return HttpResponseRedirect(reverse('judge:index'))
    else:
        return auth_views.login(request, template_name='judge/login.html')

def logout(request):
    # users should not be able to log out if they're not logged in yet
    if not request.user.is_authenticated():
        messages.error(request,
                       'You are not logged in yet.')
        return HttpResponseRedirect(reverse('judge:index'))
    else:
        return auth_views.logout(request, next_page='judge:index')

def problem_list(request):
    profile = request.user.profile

    problem_list = Problem.objects.all()
    profile_solved_list = []
    for problem in problem_list:
        profile_submission_list = problem.submission_set.filter(profile=profile)
        profile_solved = profile_submission_list.filter(status='AC').exists()
        profile_solved_list.append(profile_solved)
    problem_profile_solved_list = zip(problem_list, profile_solved_list)

    return render(request,
                  'judge/problem_list.html',
                  {'problem_profile_solved_list': problem_profile_solved_list})

def problem_detail(request, pk):
    profile = request.user.profile

    problem = get_object_or_404(Problem, pk=pk)

    # handle submission
    if request.method == 'POST':
        now = timezone.now()

        # no submissions are allowed after deadline
        if now > problem.deadline_datetime:
            messages.error(request, 'Sorry, it is already over the deadline.')
        else:
            submission = Submission(problem=problem,
                                    profile=profile,
                                    submission_datetime=now)
            submission.save()

            # judge (without waiting)
            subprocess.Popen([os.path.join(config.VIRTUALENV_BIN_DIR, 'python'),
                              os.path.join(config.JUDGE_BIN_DIR, 'judge.py'),
                              str(submission.pk)],
                             cwd=config.JUDGE_BIN_DIR)

            messages.success(request, 'Submitting. Refresh to see the results.')
        return HttpResponseRedirect(reverse('judge:problem_detail', kwargs={'pk': pk}))

    profile_submission_list = problem.submission_set.filter(profile=profile)
    profile_solved = profile_submission_list.filter(status='AC').exists()

    return render(request,
                  'judge/problem_detail.html',
                  {'problem': problem,
                   'profile_submission_list': profile_submission_list,
                   'profile_solved': profile_solved})

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

def submission_detail(request, pk):
    profile = request.user.profile

    submission = get_object_or_404(Submission, pk=pk)

    # see if this submission belongs to this profile
    if submission.profile != profile:
        messages.error(request,
                       'Permission denied.')
        return HttpResponseRedirect(reverse('judge:index'))

    return render(request,
                  'judge/submission_detail.html',
                  {'submission': submission})
