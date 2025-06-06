"""
URL configuration for gameU project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import settings
from django.conf.urls.static import static

from gameverse import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',acc_views.home,name="home"),
    path('post/edit/<int:post_id>/', acc_views.edit_post, name='edit_post'),
    path('post/delete/<int:post_id>/', acc_views.delete_post, name='delete_post'),
    path('', acc_views.login, name="login"),
    path('signup/', acc_views.signup, name="signup"),
    path('logout/', acc_views.logout_view, name="logout"),
    path('profile/',acc_views.profile,name="profile"),
    path('organizer/', acc_views.organizer, name="organizer"),
    path('organizer/edit/<int:post_id>/', acc_views.organizer_edit_post, name='organizer_edit_post'),
    path('organizer/delete/<int:post_id>/', acc_views.organizer_delete_post, name='organizer_delete_post'),

    # For tournament form posts
    path('organizer/edit-tournament/<int:form_id>/', acc_views.organizer_edit_tournament, name='organizer_edit_tournament'),
    path('organizer/delete-tournament/<int:form_id>/', acc_views.organizer_delete_tournament, name='organizer_delete_tournament'),
    path('resources/', acc_views.resources, name="resources"),
    path('upload-resource/', acc_views.upload_resource, name="upload_resource"),
    path('edit-resource/<int:pk>/', acc_views.edit_resource, name="edit_resource"),
    path('delete-resource/<int:pk>/', acc_views.delete_resource, name="delete_resource"),
    path('submit_tournament/<int:tournament_id>/', acc_views.submit_tournament_form, name='submit_tournament_form'),
    path('edit-profile/', acc_views.edit_profile, name="edit_profile"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)