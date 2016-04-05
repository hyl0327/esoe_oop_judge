import os
import sys
import django


# Debug mode
DEBUG = False


# Directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

VIRTUALENV_DIR = os.path.join(ROOT_DIR, 'virtualenv')
VIRTUALENV_BIN_DIR = os.path.join(VIRTUALENV_DIR, 'bin')

JUDGE_DIR = os.path.join(ROOT_DIR, 'judge')
JUDGE_BIN_DIR = os.path.join(JUDGE_DIR, 'bin')
JUDGE_POLICIES_DIR = os.path.join(JUDGE_DIR, 'policies')
JUDGE_PROBLEMS_DIR = os.path.join(JUDGE_DIR, 'problems')
JUDGE_STATIC_DIR = os.path.join(JUDGE_DIR, 'static')
JUDGE_STATIC_PROBLEMS_DIR = os.path.join(JUDGE_STATIC_DIR, 'problems')
JUDGE_SUBMISSIONS_DIR = os.path.join(JUDGE_DIR, 'submissions')

WEB_DIR = os.path.join(ROOT_DIR, 'web')
WEB_HTDOCS_DIR = os.path.join(WEB_DIR, 'htdocs')


# Judge related settings
JUDGE_SUBMISSION_MAX_FILE_SIZE = 10240   # in KBs
JUDGE_SUBMISSION_TIMEOUT = 5             # for each submitted file; in seconds

JUDGE_COMPILATION_TIMEOUT = 10           # for all submitted files together; in seconds

JUDGE_EXECUTION_MAX_OUTPUT_SIZE = 10240  # in KBs
JUDGE_EXECUTION_TIMEOUT = 10             # in seconds


# Web related settings
WEB_SECRET_KEY = ''

WEB_ALLOWED_HOSTS = []

WEB_INDEX_SAMPLE_PROBLEM_ID = 1


# DB related settings
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''


# Account settings
EMAIL = ''
EMAIL_PASSWORD = ''

BITBUCKET_EMAIL = ''
BITBUCKET_ACCOUNT = ''
BITBUCKET_PASSWORD = ''


# Utility functions
def set_up_django():
    sys.path.insert(0, WEB_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'esoe_oop_judge.settings'
    django.setup()
