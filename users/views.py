import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'phone', 'password')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone = re.sub(r'[^\d+]', '', phone)
        if not re.match(r'^(\+7|8)\d{10}$', phone):
            raise forms.ValidationError('Номер должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX')
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует')
        return phone


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/projects/list/')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/projects/list/')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/projects/list/')


def participants_list_view(request):
    users_list = User.objects.all().order_by('id')
    return render(request, 'users/participants.html', {'participants': users_list})