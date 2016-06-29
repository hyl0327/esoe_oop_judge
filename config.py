import os
import sys
import django


# Web settings
#
# Here are the settings for the web (Django itself).
#
# You may refer to <WEB_ESOEOOPJUDGE_DIR>/settings.py for details on how to
# correctly set them up.
#
# As a note,
#   WEB_SECRET_KEY should always be set;
#   WEB_ALLOWED_HOSTS should be set only when WEB_DEBUG is False;
#   WEB_DB_NAME/USER/PASSWORD should be set only when WEB_DB_USE_LOCAL is False;
#   WEB_DEBUG and WEB_DB_USE_LOCAL should be set to False in production.
WEB_SECRET_KEY = ''

WEB_DEBUG = False
WEB_ALLOWED_HOSTS = []

WEB_DB_USE_LOCAL = False
WEB_DB_NAME = ''
WEB_DB_USER = ''
WEB_DB_PASSWORD = ''


# Judge settings
#
# Here are the settings for the judge system.
#
# You may refer to <JUDGE_BIN_DIR>/judge.py for details on how to correctly set
# them up, but generally you don't really need to change the default values.
JUDGE_SUBMISSION_MAX_FILE_SIZE = 10240   # in KBs
JUDGE_SUBMISSION_TIMEOUT = 5             # in seconds (for each submitted file)

JUDGE_COMPILATION_TIMEOUT = 10           # in seconds (for all files to be compiled together)

JUDGE_EXECUTION_MAX_OUTPUT_SIZE = 10240  # in KBs
JUDGE_EXECUTION_TIMEOUT = 10             # in seconds


# Bitbucket settings
#
# Here are the settings for the Bitbucket account, which will be used by the
# judge system.
BITBUCKET_EMAIL = ''
BITBUCKET_ACCOUNT = ''
BITBUCKET_PASSWORD = ''


# Directories (don't change these unless you know what you're doing!)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

VIRTUALENV_DIR = os.path.join(ROOT_DIR, 'virtualenv')
VIRTUALENV_BIN_DIR = os.path.join(VIRTUALENV_DIR, 'bin')

WEB_DIR = os.path.join(ROOT_DIR, 'web')
WEB_ESOEOOPJUDGE_DIR = os.path.join(WEB_DIR, 'esoe_oop_judge')
WEB_JUDGE_DIR = os.path.join(WEB_DIR, 'judge')
WEB_HTDOCS_DIR = os.path.join(WEB_DIR, 'htdocs')

JUDGE_DIR = os.path.join(ROOT_DIR, 'judge')
JUDGE_BIN_DIR = os.path.join(JUDGE_DIR, 'bin')
JUDGE_POLICIES_DIR = os.path.join(JUDGE_DIR, 'policies')
JUDGE_PROBLEMS_DIR = os.path.join(JUDGE_DIR, 'problems')
JUDGE_STATIC_DIR = os.path.join(JUDGE_DIR, 'static')
JUDGE_STATIC_PROBLEMS_DIR = os.path.join(JUDGE_STATIC_DIR, 'problems')
JUDGE_SUBMISSIONS_DIR = os.path.join(JUDGE_DIR, 'submissions')

UTILITIES_DIR = os.path.join(ROOT_DIR, 'utilities')

DOCS_DIR = os.path.join(ROOT_DIR, 'docs')


# Utility functions (don't change these unless you know what you're doing!)
def set_up_django():
    sys.path.insert(0, WEB_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'esoe_oop_judge.settings'
    django.setup()
