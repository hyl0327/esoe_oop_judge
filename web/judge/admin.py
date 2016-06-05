from django.contrib import admin

from .models import Problem, RequiredFile, Profile, Submission


class RequiredFileInline(admin.TabularInline):
    model = RequiredFile

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'title',
        'deadline_datetime'
    ]
    inlines = [
        RequiredFileInline
    ]

@admin.register(RequiredFile)
class RequiredFileAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'problem',
        'filename',
        'via'
    ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'name'
    ]
    filter_horizontal = [
        'solved_problems'
    ]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'problem',
        'profile',
        'status',
        'submission_datetime'
    ]
