from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import *
from .forms import *
# from .forms import *
import os
from django.conf import settings
def user_can_edit(user, post):
    return post.user == user or user.profile.role == 'admin'


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')  # This will be 'on' if checked

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect('login')

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            auth_login(request, user)

            # Set session expiry
            if remember == 'on':
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Session expires on browser close

            messages.success(request, f"Welcome back, {user.username}!")

            profile = user.profile
            if profile.role == 'admin':
                return redirect('home')
            elif profile.role == 'organizer':
                return redirect('organizer')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, "login/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

# Signup Page
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # from dropdown
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create profile with role
        User_Profile.objects.create(user=user, role=role)

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, template_name="login/signup.html")

@login_required
def home(request):
    if request.user.profile.role not in ['user', 'admin','organizer']:
        return HttpResponseForbidden("You do not have permission to access this page.")
    posts = Post.objects.all().order_by('-timestamp')
    for post in posts:
        post.can_edit = user_can_edit(request.user, post)
    if request.method == 'POST':
        if 'like_post' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return redirect('home')

        elif 'contents' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.post = post
                new_comment.save()
                return redirect('home')

        else:
            # Handle post creation
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                new_post = post_form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect('home')
    post_form = PostForm()
    return render(request, 'home/home.html', {
    'post': posts,
    'post_form': post_form,
})

# Edit and delete in home
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not user_can_edit(request.user, post):
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'home/edit_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not user_can_edit(request.user, post):
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'home/delete_post.html', {'post': post})





#RESOURCE SECTION=====
def resources(request):
    texts = Resources.objects.filter(file_type='Text').order_by('-date_uploaded')
    photos = Resources.objects.filter(file_type='Photo').order_by('-date_uploaded')
    files = Resources.objects.filter(file_type='PDF').order_by('-date_uploaded')
    videos = Resources.objects.filter(file_type='Video').order_by('-date_uploaded')

    context = {
        'text_resources': texts,
        'photo_resources': photos,
        'file_resources': files,
        'video_resources': videos,
    }

    return render(request, template_name="home/resources.html", context=context)

@login_required
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.user = request.user  # associate with current user
            resource.save()
            messages.success(request, "Resource uploaded successfully!")
            return redirect('resources')
    else:
        form = ResourceForm()
    return render(request, 'home/upload_resource.html', {'form': form})


@login_required
def edit_resource(request, pk):
    resource = get_object_or_404(Resources, pk=pk, user=request.user)
    if resource.user != request.user and request.user.profile.role != 'admin':
        messages.error(request, "You are not authorized to edit this resource.")
        return redirect('resources')
    form = ResourceForm(request.POST or None, request.FILES or None, instance=resource)
    if form.is_valid():
        form.save()
        messages.success(request, "Resource updated successfully!")
        return redirect('resources')
    return render(request, 'home/upload_resource.html', {'form': form, 'edit': True})

@login_required
def delete_resource(request, pk):
    resource = get_object_or_404(Resources, pk=pk)



    if resource.user != request.user and request.user.profile.role != 'admin':
        messages.error(request, "You are not authorized to delete this resource.")
        return redirect('resources')

    if request.method == 'POST':
        resource.delete()
        messages.success(request, "Resource deleted.")
        return redirect('resources')

    return render(request, 'home/delete_resource.html', {'resource': resource})

#END of RESOURCES SECTION=====





#organizer
@login_required
def organizer(request):
    if request.user.profile.role not in ['organizer', 'admin','user']:
        return HttpResponseForbidden("You do not have permission to access this page.")
    post_form = PostForm()
    tournament_form = TournamentPostForm()

    registrations = TournamentRegistration.objects.filter(tournament__organizer=request.user)

    if request.method == 'POST':
        post_type = request.POST.get('post_type')

        if post_type == 'image':
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('organizer')

        elif post_type == 'tournament':
            tournament_form = TournamentPostForm(request.POST)
            if tournament_form.is_valid():
                tform = tournament_form.save(commit=False)
                tform.organizer = request.user
                fields_str = tournament_form.cleaned_data.get('fields_required', '')
                tform.fields_required = [f.strip() for f in fields_str.split(',') if f.strip()]
                tform.save()
                return redirect('organizer')
            else:
                print("Tournament Form Errors:", tournament_form.errors)

    posts = Post.objects.filter(user=request.user).order_by('-timestamp')
    tournament_posts = TournamentFormPost.objects.all().order_by('-created_at')  # Show all tournaments

    return render(request, 'home/organizer.html', {
        'post_form': post_form,
        'tournament_form': tournament_form,
        'posts': posts,
        'tournament_posts': tournament_posts,
        'registrations': registrations,
    })

@login_required
def submit_tournament_form(request, tournament_id):
    tournament = get_object_or_404(TournamentFormPost, id=tournament_id)

    if request.user.profile.role != 'user':
        return HttpResponseForbidden("Only normal users can register.")

    if request.method == 'POST':
        field_data = {}
        
        for i in range(1, tournament.num_players_per_team + 1):
            player_data = {}
            for field in tournament.fields_required:
                field_value = request.POST.get(f'player_{i}_{field}')
                if not field_value:
                    messages.error(request, f"Missing value for Player {i} - {field}")
                    return redirect('organizer')
                player_data[field] = field_value
            
            field_data[f'Player {i}'] = player_data

        registration = TournamentRegistration(
            user=request.user,
            tournament=tournament,
            data=field_data
        )
        registration.save()
        messages.success(request, "Registration submitted successfully.")
        return redirect('home') 


@login_required
def organizer_edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('organizer')
    else:
        form = PostForm(instance=post)
    return render(request, 'home/edit_post.html', {'form': form})

@login_required
def organizer_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('organizer')
    return render(request, 'home/delete_post.html', {'post': post})

@login_required
def organizer_edit_tournament(request, form_id):
    form_post = get_object_or_404(TournamentFormPost, id=form_id, organizer=request.user)
    if request.method == 'POST':
        form = TournamentPostForm(request.POST, instance=form_post)
        if form.is_valid():
            tform = form.save(commit=False)
            fields_str = form.cleaned_data.get('fields_required', '')
            tform.fields_required = [f.strip() for f in fields_str.split(',') if f.strip()]
            tform.save()
            return redirect('organizer')
    else:
        form = TournamentPostForm(instance=form_post)
    return render(request, 'home/edit_tournament.html', {'form': form})

@login_required
def organizer_delete_tournament(request, form_id):
    form_post = get_object_or_404(TournamentFormPost, id=form_id, organizer=request.user)
    if request.method == 'POST':
        form_post.delete()
        return redirect('organizer')
    return render(request, 'home/delete_tournament.html', {'form_post': form_post})






# @login_required
# def register_tournament(request, tform_id):
#     tournament = get_object_or_404(TournamentFormPost, id=tform_id)
#     if request.method == 'POST':
#         form = DynamicTournamentRegistrationForm(request.POST, dynamic_fields=tournament.required_fields)
#         if form.is_valid():
#             TournamentRegistration.objects.create(
#                 tournament=tournament,
#                 submitted_by=request.user,
#                 submission_data=form.cleaned_data
#             )
#             messages.success(request, "Successfully registered for the tournament.")
#             return redirect('organizer')
#     else:
#         form = DynamicTournamentRegistrationForm(dynamic_fields=tournament.required_fields)

#     return render(request, 'home/tournament_register.html', {
#         'tournament': tournament,
#         'form': form
#     })




# def register_tournament(request, pk):
#     tournament = TournamentFormPost.objects.get(pk=pk)
#     # Logic to show a form or save registration
#     return render(request, 'register_tournament.html', {'tournament': tournament})

# @login_required
# def profile(request):
#      return render(request, "home/profile.html")
@login_required
def profile(request):
    # Get the logged-in user's profile
    user_profile = get_object_or_404(User_Profile, user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, template_name='home/profile.html', context=context)


# @login_required
# def edit_profile(request):
#     user_form = UserForm(instance=request.user)
#     profile_form = UserProfileForm(instance=request.user.profile)

#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('profile', username=request.user.username)

#     return render(request, 'home/edit_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })
@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile  # this is User_Profile object

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # or wherever your profile page is
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'home/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    