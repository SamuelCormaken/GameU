from django import forms
from django.forms import ModelForm
from .models import *

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resources
        exclude = ['user', 'date_uploaded']

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'likes']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'post']

class OrganizerPostForm(forms.ModelForm):
    class Meta:
        model = OrganizerPost
        fields = ['image', 'description']

class TournamentPostForm(forms.ModelForm):
    fields_required = forms.CharField(help_text="Comma-separated field names (e.g. Player1, Player2)")

    class Meta:
        model = TournamentFormPost
        fields = ['title', 'description', 'num_players_per_team', 'fields_required']

class DynamicTournamentRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dynamic_fields = kwargs.pop('dynamic_fields', [])
        super().__init__(*args, **kwargs)
        for field in dynamic_fields:
            self.fields[field] = forms.CharField(label=field, max_length=100)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = ['image']
