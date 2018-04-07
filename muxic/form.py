from django.contrib.auth import authenticate
from django.contrib.auth.forms import UsernameField, UserModel
from django.contrib.auth.models import *
from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from django.utils.text import capfirst

from muxic.models import UserProfile


class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput,
        max_length=254,
    )
    email = forms.CharField(
        widget=forms.EmailInput,
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
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean_confirm_password(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if len(password) < 6:
            print("check1")
            raise forms.ValidationError("Mật khẩu từ 6 đến 24 kí tự!")

        elif len(password) > 24:
            print("check2")
            raise forms.ValidationError("Mật khẩu từ 6 đến 24 kí tự!")

        elif password != confirm_password:
            raise forms.ValidationError("Mật khẩu bạn nhập không trùng!")
            # raise ValidationError("Mật khẩu bạn nhập không trùng!")
        else:
            return confirm_password

    # def clean_password(self, passw, confirmpass):
    #     cleaned_data = super(UserForm, self).clean()
    #
    #     password = passw
    #     confirm_password = confirmpass
    #     if len(password) < 6:
    #         raise forms.ValidationError("Mật khẩu từ 6 đến 24 kí tự!")
    #
    #     if len(password) > 24:
    #         raise forms.ValidationError("Mật khẩu từ 6 đến 24 kí tự!")

    def clean_username(self):
        clean_data = super(UserForm, self).clean()
        username = clean_data.get('username')
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có ký tự đặc biệt!")

        if len(username) < 6:
            raise forms.ValidationError("Tên tài khoản từ 6 đến 24 kí tự!")

        if len(username) > 24:
            raise forms.ValidationError("Tên tài khoản từ 6 đến 24 kí tự!")

        try:
            UserProfile.objects.get(user__username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def clean_email(self):
        clean_data = super(UserForm, self).clean()
        email = clean_data.get('email')
        # if not validate_email(email):
        #
        #     raise forms.ValidationError("Email không hợp lệ!")
        try:
            UserProfile.objects.get(user__email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError("Email đã tồn tại")

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
