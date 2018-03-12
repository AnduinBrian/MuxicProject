from django.contrib.auth import authenticate
from django.contrib.auth.forms import UsernameField, UserModel
from django.contrib.auth.models import User
from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.utils.text import capfirst


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput,
        max_length=254,
    )
    email = forms.CharField(
        widget=forms.EmailInput,
        max_length=254,
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        clean_data = super(RegisterForm, self).clean()
        password = clean_data.get("password")
        confirm_password = clean_data.get("confirm_password")

        if len(password) < 6 and len(password) > 24:
            raise forms.ValidationError("Mật khẩu từ 6 đến 24 kí tự!")

        if password != confirm_password:
            raise forms.ValidationError("Mật khẩu bạn nhập không trùng!")

    def clean_username(self):
        clean_data = super(RegisterForm, self).clean()
        username = clean_data.get('username')
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có ký tự đặc biệt!")

        if len(username) < 6 and len(username) > 24:
            raise forms.ValidationError("Tên tài khoản từ 6 đến 24 kí tự!")

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def clean_email(self):
        clean_data = super(RegisterForm, self).clean()
        email = clean_data.get('email')
        if not validate_email(email):

            raise forms.ValidationError("Email không hợp lệ!")

        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError("Email đã tồn tại")


