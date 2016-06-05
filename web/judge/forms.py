from .models import Profile

from django.forms import ModelForm


class ProfileUpdateBitbucketForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bitbucket_account', 'bitbucket_repository']
