from django import forms
from django.core.exceptions import ValidationError

from .models import User, UserConfirmation


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

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
        return user


class CodeVerifyForm(forms.ModelForm):
    class Meta:
        model = UserConfirmation
        fields = ['code']

    
class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        print('login email ', cleaned_data)

        email = cleaned_data.get('email', None)
        password = cleaned_data.get('password', None)
        if email is None:
            raise ValidationError('email maydoni bo\'sh bo\'lishi mumkin emas')
        if email and not User.objects.filter(email=email).exists():
            raise ValidationError("bunday email va parolga ega foydalanuvchi topilmadi")
        
        if password is None:
            raise ValidationError('password maydoni bo\'sh bo\'lishi mumkin emas')
        
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise ValidationError("password xato")
        except User.DoesNotExist:
            raise ValidationError('bunday user mavjud emas')
        
        return cleaned_data
    

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        email = self.cleaned_data['email']

        if email is None:
            raise ValidationError("email maydoni bo'sh")
        if email and not User.objects.filter(email=email).exists():
            raise ValidationError('bunday emailli user mavjud emas')
        return email
    

class ResetPasswordForm(forms.Form):
    password = forms.CharField()
    confirm_password = forms.CharField()

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password is None:
            raise ValidationError("password maydoni bo'sh")
        if password != confirm_password:
            raise ValidationError("passwordlar bir xil emas")
        if len(password) < 8:
            raise ValidationError("passwordlar kamida 8 ta belgidan kam bo'lmasligi kerak")
        if password.isdigit():
            raise ValidationError("password to'liq raqamlardan iborat bo'lmasligi kerak")
        
        return self.cleaned_data
    