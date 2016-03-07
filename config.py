import os
import sys
import django


# Root of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# Common settings
EMAIL = 'esoe.oop.judge@gmail.com'
EMAIL_PASSWORD = 'qfTurFvx6u1ZV997H6gZ'

BITBUCKET_EMAIL = 'esoe.oop.judge@gmail.com'
BITBUCKET_ACCOUNT = 'esoe_oop_judge'
BITBUCKET_PASSWORD = 'qfTurFvx6u1ZV997H6gZ'


# Virtualenv related settings
VIRTUALENV_DIR = os.path.join(ROOT_DIR, 'virtualenv')

VIRTUALENV_BIN_DIR = os.path.join(VIRTUALENV_DIR, 'bin')


# DB related settings
DB_NAME = 'esoe_oop_judge'
DB_USER = 'esoe_oop_judge'
DB_PASSWORD = 'zxt5t5NuT4HETiKl'


# Web related settings
WEB_DIR = os.path.join(ROOT_DIR, 'web')

WEB_SECRET_KEY = '^1&vzcf@^j8&lyaxs1hus6k69=aw4$x*#&794g&abj)=be6(gr'

WEB_HOST = 'oopjudge.cklab.org'

WEB_STATIC_ROOT = os.path.join(WEB_DIR, 'static')


# Judge related settings
JUDGE_DIR = os.path.join(ROOT_DIR, 'judge')

JUDGE_BIN_DIR = os.path.join(JUDGE_DIR, 'bin')
JUDGE_POLICIES_DIR = os.path.join(JUDGE_DIR, 'policies')
JUDGE_PROBLEMS_DIR = os.path.join(JUDGE_DIR, 'problems')
JUDGE_STATIC_DIR = os.path.join(JUDGE_DIR, 'static')
JUDGE_STATIC_PROBLEMS_DIR = os.path.join(JUDGE_STATIC_DIR, 'problems')
JUDGE_SUBMISSIONS_DIR = os.path.join(JUDGE_DIR, 'submissions')

JUDGE_SUBMISSION_MAX_FILE_SIZE = 10240   # in KBs
JUDGE_SUBMISSION_TIMEOUT = 5             # for each submitted file; in seconds
JUDGE_COMPILATION_TIMEOUT = 10           # for all submitted files together; in seconds
JUDGE_EXECUTION_MAX_OUTPUT_SIZE = 10240  # in KBs
JUDGE_EXECUTION_TIMEOUT = 10             # in seconds


# Utility functions
def set_up_django():
    sys.path.insert(0, WEB_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esoe_oop_judge.settings')
    django.setup()
