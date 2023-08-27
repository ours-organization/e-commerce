from django import forms
from django.core.exceptions import ValidationError

from .models import User
from apps.common.utility import send_mail


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email is None:
            raise ValidationError("maydon bo'sh bo'lishi mumkin emas")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("bu email allaqachon mavjud")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("password va confirm passwordd bir xil emas")
        if cleaned_data.get('first_name') in password or cleaned_data.get('last_name') in password:
            raise ValidationError("password first name yoki last name malumotlari bilan bir xil bo'lmasligi kerak")
        if password.isdigit():
            raise ValidationError("password to'liq raqamlardan iborat bo'lmasligi kerak")
        if len(password) < 8:
            raise ValidationError("password kamida 8 ta belgidan iborat bo'lishi kerak")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        user.set_password(self.cleaned_data.get('password'))

        if user.email:
            code = user.create_verify_code(user.email)
            print('code ', code)
            send_mail(user.email, code)
        return user


class CodeVerifyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']