#!/usr/bin/env python3

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
config.set_up_django()

from judge.models import Problem, Profile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--users',
                        help='Limit results to specified users only',
                        nargs='*',
                        metavar='USER')
    parser.add_argument('-p', '--problems',
                        help='Limit results to specified problems only',
                        type=int,
                        nargs='*',
                        metavar='PROBLEM')
    args = parser.parse_args()

    if args.problems is None:
        problems = Problem.objects.all()
    else:
        problems = Problem.objects.filter(pk__in=args.problems)
    if args.users is None:
        profiles = Profile.objects.all()
    else:
        profiles = Profile.objects.filter(user__username__in=args.users)
    for profile in profiles:
        print(profile)
        if args.problems is None:
            profile_solved_problems = profile.solved_problems.all()
        else:
            profile_solved_problems = profile.solved_problems.filter(pk__in=args.problems)
        for problem in problems:
            print('\t{}:{}{}'.format(
                problem,
                ' ' * (max(40 - len(problem.__str__()), 5)),
                'Solved' if problem in profile_solved_problems else 'Unsolved'
            ))

if __name__ == '__main__':
    main()
