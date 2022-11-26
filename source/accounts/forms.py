from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username'
    )
    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput
    )
    next = forms.CharField(
        required=False,
        widget=forms.HiddenInput
    )

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password'
        )


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        strip=False,
        required=True,
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label='Confirm password',
        strip=False,
        required=True,
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password',
            'password_confirm'
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Passwords dont match!')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user
