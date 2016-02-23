from django.db import models

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

    time_limit = models.IntegerField()    # in ms
    memory_limit = models.IntegerField()  # in MBs

    deadline_datetime = models.DateTimeField()

    # should it be judged by an answer file (as traditionally) or an executable?
    judged_by = models.CharField(max_length=1,
                                 choices=(('F', 'File'),
                                          ('E', 'Executable')))
    testcase_amount = models.IntegerField()

    def __str__(self):
        return '{:s}'.format(self.title)

    class Meta:
        ordering = ['pk']

class RequiredFile(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    # where should the file come from?
    via = models.CharField(max_length=1,
                           choices=(('S', 'Submitted'),
                                    ('P', 'Provided')))
    filename = models.CharField(max_length=32)

    def __str__(self):
        return '{:s} (Problem={:s})'.format(self.filename,
                                            str(self.problem))

    class Meta:
        ordering = ['problem__pk', 'via', 'filename']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Bitbucket settings
    bitbucket_account = models.CharField(max_length=32, blank=True)
    bitbucket_repository = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return '#{:d} (User={:s})'.format(self.pk,
                                          str(self.user))

    class Meta:
        ordering = ['user__username']

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    status = models.CharField(max_length=2,
                              choices=(('SE', 'Submission Error'),
                                       ('JU', 'Judging'),
                                       ('AC', 'Accepted'),
                                       ('PA', 'Partially Accepted'),
                                       ('TL', 'Time Limit Exceeded'),
                                       ('ML', 'Memory Limit Exceeded'),
                                       ('RE', 'Runtime Error'),
                                       ('CE', 'Compile Error')),
                              blank=True)
    score = models.IntegerField(null=True, blank=True, db_index=True)
    running_time = models.IntegerField(null=True, blank=True)  # in ms

    submission_datetime = models.DateTimeField()

    def __str__(self):
        return '#{:d} (Problem={:s}, Profile={:s})'.format(self.pk,
                                                           str(self.problem),
                                                           str(self.profile))

    class Meta:
        ordering = ['-pk']
