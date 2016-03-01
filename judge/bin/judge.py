#!/usr/bin/env python3

import os
import sys
import subprocess

import django

# set up Django
sys.path.insert(0, r'../../web')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esoe_oop_judge.settings')
django.setup()

from django.conf import settings

from judge.models import Submission

submission_id = None
submission = None
problem = None
profile = None

submission_id_dir = None

provided_filenames = None
submitted_filenames = None

def get_submitted_files():
    global submission_id, submission, problem, profile
    global submission_id_dir
    global provided_filenames, submitted_filenames

    # this is safe as bitbucket settings are guaranteed (at model level) to
    # contain only letters, numbers, hyphens and underscores
    bitbucket_base_url = 'https://api.bitbucket.org/1.0/repositories/{:s}/{:s}/raw/master/{:d}/'
    bitbucket_base_url = bitbucket_base_url.format(profile.bitbucket_account,
                                                   profile.bitbucket_repository,
                                                   problem.pk)

    for filename in submitted_filenames:
        try:
            bitbucket_url = bitbucket_base_url + filename

            subprocess.run(['curl',
                            '--silent',
                            '--show-error',
                            '--fail',
                            '--max-filesize', str(settings.JUDGE_SUBMISSION_MAX_FILESIZE),
                            '--user', '{:s}:{:s}'.format(settings.JUDGE_BITBUCKET_EMAIL,
                                                         settings.JUDGE_BITBUCKET_PASSWORD),
                            bitbucket_url,
                            '--output', filename],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,
                           timeout=settings.JUDGE_SUBMISSION_TIMEOUT,
                           check=True)
        except subprocess.TimeoutExpired as e:
            submission.detail_message = 'Submission of \'{:s}\' timed out.'.format(filename),

            submission.status = 'SE'
            submission.save()
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            if e.returncode == 22:
                submission.detail_message = ('\'{:s}\' was not found at \'{:s}\''
                                             ' (if the file actually exists,'
                                             ' then you should check if you have'
                                             ' made the repository accessible to'
                                             ' the judge\'s Bitbucket account;'
                                             ' for details, please refer to the'
                                             ' instructions on the home page).').format(filename,
                                                                                        bitbucket_url)
            elif e.returncode == 63:
                submission.detail_message = ('\'{:s}\' exceeds the maximum'
                                             ' file size.').format(filename)
            else:
                submission.detail_message = ('The following error(s) occurred during'
                                             ' the submission of \'{:s}\':\n\n{:s}').format(filename,
                                                                                            e.stderr)

            submission.status = 'SE'
            submission.save()
            sys.exit(1)

def compile_submitted_files():
    global submission_id, submission, problem, profile
    global submission_id_dir
    global provided_filenames, submitted_filenames

    try:
        # only submitted source files should be compiled
        subprocess.run((['javac'] + submitted_filenames),
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       universal_newlines=True,
                       timeout=settings.JUDGE_COMPILATION_TIMEOUT,
                       check=True)
    except subprocess.TimeoutExpired as e:
        submission.detail_message = 'Compilation timed out.'

        submission.status = 'CE'
        submission.save()
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        submission.detail_message = ('The following error(s) occurred during'
                                     ' the compilation:\n\n{:s}').format(e.stderr)

        submission.status = 'CE'
        submission.save()
        sys.exit(1)

def main():
    global submission_id, submission, problem, profile
    global submission_id_dir
    global provided_filenames, submitted_filenames

    if len(sys.argv) != 2:
        print('usage: {:s} submission_id'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    # basic information
    submission_id = int(sys.argv[1])
    submission = Submission.objects.get(pk=submission_id)
    problem = submission.problem
    profile = submission.profile

    submission_id_dir = os.path.join(settings.JUDGE_SUBMISSIONS_DIR, str(submission_id))

    provided_filenames = [f.filename for f in problem.requiredfile_set.filter(via='P')]
    submitted_filenames = [f.filename for f in problem.requiredfile_set.filter(via='S')]

    # create submission_id_dir and chdir to it
    os.mkdir(submission_id_dir, 0o755)
    os.chdir(submission_id_dir)

    # redirect stdout and stderr
    sys.stdout = open('stdout', 'w')
    sys.stderr = open('stderr', 'w')

    # get submitted files and compile them
    get_submitted_files()
    submission.status = 'CO'
    submission.save()
    compile_submitted_files()

if __name__ == '__main__':
    main()
