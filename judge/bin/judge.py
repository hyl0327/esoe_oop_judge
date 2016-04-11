#!/usr/bin/env python3

import os
import sys
import shlex
import shutil
import subprocess
import resource

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config

config.set_up_django()
from judge.models import Submission

submission = None
problem = None
profile = None

def get_submitted_files():
    global submission, problem, profile

    # Bitbucket url base string; this is safe as Bitbucket settings are
    # guaranteed (at model level) to be slugs
    bitbucket_url_base = (
        'https://api.bitbucket.org/1.0/repositories/{}/{}/raw/master/{}/{}'
    ).format(profile.bitbucket_account,
             profile.bitbucket_repository,
             problem.pk,
             '{}')
    # command base string
    cmd_base = (
        'curl'
        ' --silent'
        ' --show-error'
        ' --fail'
        ' --max-filesize {}'
        ' --user {}:{}'
        ' {}'
        ' --output {}'
    ).format(shlex.quote(str(config.JUDGE_SUBMISSION_MAX_FILE_SIZE * 1024)),
             shlex.quote(config.BITBUCKET_EMAIL),
             shlex.quote(config.BITBUCKET_PASSWORD),
             '{}',
             '{}')
    # get submitted files
    submitted_filenames = [f.filename for f in problem.requiredfile_set.filter(via='S')]
    for filename in submitted_filenames:
        bitbucket_url = bitbucket_url_base.format(filename)
        cmd = cmd_base.format(shlex.quote(bitbucket_url),
                              shlex.quote(filename))
        try:
            subprocess.run(shlex.split(cmd),
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,
                           timeout=config.JUDGE_SUBMISSION_TIMEOUT,
                           check=True)
        except subprocess.TimeoutExpired as e:
            submission.status = 'SE'
            submission.detailed_messages = (
                'The submission of <code>{}</code> timed out.'
            ).format(filename)
            submission.save()
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            if e.returncode == 22:
                submission.status = 'SE'
                submission.detailed_messages = (
                    '<code>{0}</code> was not found at <code>{1}/{0}</code> in'
                    ' your repository.\n\n'
                    'Please make sure you have correctly set up the Bitbucket'
                    ' settings in your profile, made the repository accessible'
                    ' to the judge\'s Bitbucket account, and that the file'
                    ' actually exists.\n\n'
                    'For details, please refer to the guidelines on the home'
                    ' page.'
                ).format(filename,
                         problem.pk)
            elif e.returncode == 63:
                submission.status = 'SE'
                submission.detailed_messages = (
                    '<code>{}</code> exceeds the maximum file size limit'
                    ' ({} KBs).'
                ).format(filename,
                         config.JUDGE_SUBMISSION_MAX_FILE_SIZE)
            else:
                submission.status = 'SE'
                submission.detailed_messages = (
                    'The following errors occurred during the submission of'
                    ' <code>{}</code>:'
                ).format(filename)
                submission.detailed_messages_stderr = e.stderr
            submission.save()
            sys.exit(1)

def compile():
    global submission, problem, profile

    # copy Main.java and provided files to here
    problem_id_dir = os.path.join(config.JUDGE_PROBLEMS_DIR, str(problem.pk))
    problem_id_provided_dir = os.path.join(config.JUDGE_STATIC_PROBLEMS_DIR, str(problem.pk))
    provided_filenames = [f.filename for f in problem.requiredfile_set.filter(via='P')]
    shutil.copyfile(os.path.join(problem_id_dir, 'Main.java'),
                    os.path.join(os.getcwd(), 'Main.java'))
    for filename in provided_filenames:
        shutil.copyfile(os.path.join(problem_id_provided_dir, filename),
                        os.path.join(os.getcwd(), filename))

    # compile
    cmd = (
        'javac'
        ' Main.java'
    )
    try:
        subprocess.run(shlex.split(cmd),
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       universal_newlines=True,
                       timeout=config.JUDGE_COMPILATION_TIMEOUT,
                       check=True)
    except subprocess.TimeoutExpired as e:
        submission.status = 'CE'
        submission.detailed_messages = (
            'Compilation timed out.'
        )
        submission.save()
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        submission.status = 'CE'
        submission.detailed_messages = (
            'The following errors occurred during compilation:'
        )
        submission.detailed_messages_stderr = e.stderr
        submission.save()
        sys.exit(1)

def set_rlimit_fsize():
    # set the maximum output size limit (in bytes)
    resource.setrlimit(resource.RLIMIT_FSIZE,
                       (config.JUDGE_EXECUTION_MAX_OUTPUT_SIZE * 1024,
                        config.JUDGE_EXECUTION_MAX_OUTPUT_SIZE * 1024))
def execute():
    global submission, problem, profile

    # execute
    # TODO: timeout
    cmd = (
        'java'
        ' -Djava.security.manager'
        ' -Djava.security.policy=={}'
        ' Main'
    ).format(shlex.quote(os.path.join(config.JUDGE_POLICIES_DIR, 'default.policy')))
    try:
        # FIXME:
        #
        # As JVM doesn't seem to handle SIGXFSZ properly, the program won't
        # stop running upon exceeding the maximum output size limit;
        # instead, it will continue running, but with a restriction imposed
        # by the operating system on its following output.
        #
        # Although the operating system will restrict the program's
        # following output, this is still not desired since, in this way,
        # the program won't return a special return code and hence we can't
        # catch it and show an error message to the user.
        problem_id_dir = os.path.join(config.JUDGE_PROBLEMS_DIR, str(problem.pk))
        with open(os.path.join(problem_id_dir, 'input.txt')) as fin, open('output.txt', 'w') as fout:
            subprocess.run(shlex.split(cmd),
                           stdin=fin,
                           stdout=fout,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,
                           timeout=config.JUDGE_EXECUTION_TIMEOUT,
                           check=True,
                           preexec_fn=set_rlimit_fsize)
    except subprocess.TimeoutExpired as e:
        submission.status = 'RE'
        submission.detailed_messages = (
            'Execution timed out.'
        )
        submission.save()
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        submission.status = 'RE'
        submission.detailed_messages = (
            'The following errors occurred during execution:'
        )
        submission.detailed_messages_stderr = e.stderr
        submission.save()
        sys.exit(1)

    # judge
    cmd = (
        'diff'
        ' {}'
        ' {}'
    ).format(shlex.quote('output.txt'),
             shlex.quote(os.path.join(problem_id_dir, 'answer.txt')))
    try:
        # diff returns an error code when there're any differences
        p = subprocess.run(shlex.split(cmd),
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,
                           check=True)
    except subprocess.CalledProcessError as e:
        submission.status = 'WA'
        submission.save()
        sys.exit(1)
    submission.status = 'AC'
    submission.save()

def main():
    global submission, problem, profile

    if len(sys.argv) != 2:
        print('usage: {} submission_id'.format(sys.argv[0]),
              file=sys.stderr)
        sys.exit(1)

    submission_id = int(sys.argv[1])

    # create submission_id_dir and chdir to it
    submission_id_dir = os.path.join(config.JUDGE_SUBMISSIONS_DIR, str(submission_id))
    os.mkdir(submission_id_dir)
    os.chdir(submission_id_dir)

    # redirect stdout and stderr
    sys.stdout = open('stdout', 'w')
    sys.stderr = open('stderr', 'w')

    # basic information
    submission = Submission.objects.get(pk=submission_id)
    problem = submission.problem
    profile = submission.profile

    # get submitted files
    get_submitted_files()

    # compile
    submission.status = 'CO'
    submission.save()
    compile()

    # execute
    submission.status = 'JU'
    submission.save()
    execute()

if __name__ == '__main__':
    main()
