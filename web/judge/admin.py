from django.contrib import admin

from .models import Problem, RequiredFile, Profile, Submission

admin.site.register(Problem)
admin.site.register(RequiredFile)
admin.site.register(Profile)
admin.site.register(Submission)
