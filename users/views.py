from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse

from team_finder.constants import PAGINATION_PAGE_SIZE
from users.forms import RegistrationForm
from users.models import User


def register_view(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect(reverse('projects:project_list'))
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect(reverse('projects:project_list'))
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('projects:project_list'))


def participants_list_view(request):
    users_list = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users_list, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/participants.html', {'participants': page_obj})