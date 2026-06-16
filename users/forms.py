import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm

from users.models import User

User = get_user_model()


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


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone = re.sub(r'[^\d+]', '', phone)
        if not re.match(r'^(\+7|8)\d{10}$', phone):
            raise forms.ValidationError('Номер должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX')
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        if User.objects.filter(phone=phone).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует')
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url:
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url
    