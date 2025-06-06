from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
admin.site.register([User_Profile, Post, Comment, Resources, TournamentFormPost,TournamentRegistration])