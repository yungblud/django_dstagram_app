from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    # Validation용
    # views.py의 is_valid()함수 가 쓰일때 자동적으로 validate
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Password not match..")
        if len(cd['password2']) < 3:
            raise forms.ValidationError("비밀번호는 4글자 이상이어야 합니다.")
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if len(cd['username']) < 3:
            raise forms.ValidationError("이름은 세글자 이상이여야 합니다.")
        return cd['username']

    def clean_email(self):
        cd = self.cleaned_data
        if len(cd['email']) == 0:
            raise forms.ValidationError("이메일을 입력하여 주세요.")
        if not "@" in cd['email']:
            raise forms.ValidationError("이메일주소만 사용하여주세요.")
        return cd['email']