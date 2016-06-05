#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
config.set_up_django()

from django.contrib.auth.models import User
from judge.models import Profile


def main():
    if len(sys.argv) != 2:
        print('usage: {} filename'.format(sys.argv[0]),
              file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        for line in f:
            student_id, name = line.split(',')

            # wipe out the trailing '\n'
            name = name[:-1]

            # create user, with its password being the same as its student ID,
            # and its email being its NTU mail
            user = User.objects.create_user(username=student_id,
                                            email=(student_id + '@ntu.edu.tw'),
                                            password=student_id)
            user.save()

            # create its corresponding profile
            profile = Profile(user=user, name=name)
            profile.save()

if __name__ == '__main__':
    main()
