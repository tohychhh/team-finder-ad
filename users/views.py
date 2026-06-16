from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, redirect, render

from projects.service import paginate_queryset
from users.forms import ProfileEditForm, RegistrationForm
from users.models import User


def register_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect('projects:project_list')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('projects:project_list')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('projects:project_list')


def participants_list_view(request):
    users_list = User.objects.all().order_by('-date_joined')
    page_obj = paginate_queryset(users_list, request)
    return render(request, 'users/participants.html', {'participants': page_obj})


def user_detail_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    projects = user_obj.owned_projects.all()
    page_obj = paginate_queryset(projects, request)
    return render(request, 'users/user-details.html', {
        'user_obj': user_obj,
        'projects': page_obj,
    })


@login_required
def edit_profile_view(request, user_id):
    if request.user.id != user_id:
        return redirect('users:user_detail', user_id=request.user.id)
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('users:user_detail', user_id=user_id)
    else:
        form = ProfileEditForm(instance=user_obj)
    return render(request, 'users/edit_profile.html', {'form': form, 'user_obj': user_obj})


@login_required
def change_password_view(request, user_id):
    if request.user.id != user_id:
        return redirect('users:user_detail', user_id=request.user.id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:user_detail', user_id=user_id)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def redirect_to_change_password(request):
    return redirect('users:change_password', user_id=request.user.id)


@login_required
def redirect_to_edit_profile(request):
    return redirect('users:edit_profile', user_id=request.user.id)
