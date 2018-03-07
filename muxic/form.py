from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        clean_data = super(UserForm, self).clean()
        password = clean_data.get("password")
        confirm_password = clean_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Mật khẩu bạn nhập không trùng!")
