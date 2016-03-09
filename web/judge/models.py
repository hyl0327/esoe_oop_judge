from django.db import models
from django.core.validators import validate_slug

from django.contrib.auth.models import User

class Problem(models.Model):
    # is it a sample problem?
    is_sample = models.BooleanField()

    title = models.CharField(max_length=32)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()

    deadline_datetime = models.DateTimeField()

    def __str__(self):
        return '{}{}'.format('(Sample) ' if self.is_sample else '',
                             self.title)

    class Meta:
        ordering = ['pk']

class RequiredFile(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    filename = models.CharField(max_length=32)
    via = models.CharField(max_length=1,
                           choices=(('S', 'Submitted'),
                                    ('P', 'Provided')))

    def __str__(self):
        return '{} (Problem={})'.format(self.filename,
                                        str(self.problem))

    class Meta:
        ordering = ['problem__pk', 'via', 'filename']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Bitbucket settings
    bitbucket_account = models.CharField(max_length=32,
                                         blank=True,
                                         validators=[validate_slug])
    bitbucket_repository = models.CharField(max_length=32,
                                            blank=True,
                                            validators=[validate_slug])

    def __str__(self):
        return '#{} (User={})'.format(self.pk,
                                      str(self.user))

    class Meta:
        ordering = ['user__username']

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    status = models.CharField(max_length=2,
                              choices=(('SU', 'Submitting'),
                                       ('SE', 'Submission Error'),
                                       ('CO', 'Compiling'),
                                       ('CE', 'Compilation Error'),
                                       ('JU', 'Judging'),
                                       ('AC', 'Accepted'),
                                       ('NA', 'Not Accepted'),
                                       ('TL', 'Time Limit Exceeded'),
                                       ('RE', 'Runtime Error')),
                              default='SU',
                              db_index=True)
    submission_datetime = models.DateTimeField()

    detailed_messages = models.TextField(blank=True)

    def __str__(self):
        return '#{} (Problem={}, Profile={})'.format(self.pk,
                                                     str(self.problem),
                                                     str(self.profile))

    class Meta:
        ordering = ['-pk']
