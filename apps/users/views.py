import threading

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
# from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator

from .models import User
from .forms import RegisterForm, CodeVerifyForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from apps.common.utility import send_email, send_reset_email


class HomePageView(TemplateView):
    template_name = 'base.html'


class RegisterView(View):
    def post(self, request):  
        form = RegisterForm(request.POST)  
        if form.is_valid():  
            user = form.save(commit=False)  
            user.is_active = False  
            user.auth_step = User.AuthStep.FIRST_STEP
            user.save()  

            code = user.create_verify_code()
            to_email = form.cleaned_data['email']
            request.session['code'] = code

            email_thread = threading.Thread(
                target=send_email,
                args=[user, code, to_email]
            )
            email_thread.start()  
                #   bu yerga message yoziladi
            return redirect("users:code", uidb64=user.id)
        return render(request, 'register/register.html', {'form': form}) 

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register/register.html', {'form': form}) 
    

class LoginView(View):
    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                #   bu yerga message yoziladi
                return redirect('users:home')
        return render(request, "register/login.html", {'form': form})
    
    def get(self, request):
        form = LoginForm()
        return render(request, 'register/login.html', {'form': form}) 
    

class LogOutView(View):
    def post(self, request):
        logout(request)
        return redirect('users:home')
    
    def get(self, request):
        return render(request, 'register/logout.html', {})


class CodeVerifyView(View):
    def post(self, request, uidb64:str):
        User = get_user_model()
        try:
            user = User.objects.get(id=uidb64)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        code = request.session.get('code')
        print(f"user in codeverify : {user}")
        print(f"code in codeverify : {code}")
        

        if user is not None:
            form = CodeVerifyForm(data=request.POST)

            if request.POST['code'] != code:
                return HttpResponse("noto'g'ri tasdiqlash kodi")                           

            if form.is_valid(): 
                user.is_active = True
                user.auth_step = User.AuthStep.SECOND_STEP
                user.save()
                #   bu yerga message yoziladi
                return redirect('users:home')
            else:
                return HttpResponse("form in valid")
            
        return render(request, "register/codeverify.html", {'form': form})
   
    def get(self, request,  uidb64):
        form = CodeVerifyForm()
        return render(request, 'register/codeverify.html', {'form': form})

    # @staticmethod
    # def check_verify(user, code):
    #     verifies = user.verify_codes.filter(expiration_time__gte=datetime.datetime.now(), code=code, is_confirmed=False)
    #     print(f"verifies = {user.expiration_time__gte}, {user.is_confirmed},{user.code}")
    #     if not verifies.exists():
    #         return HttpResponse('xato verify code')
    #     verifies.update(is_confirmed=True)

    #     if user.auth_step == User.AuthStep.FIRST_STEP:
    #         user.auth_step = User.AuthStep.SECOND_STEP
    #         user.save()
    #     return True


class ForgotPasswordView(View):
    def post(self, request):
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                reset_password_url = reverse('users:reset_password', kwargs={'uidb64': user.id, 'token': token})
                reset_password_link = self.request.build_absolute_uri(reset_password_url)
                email_thread = threading.Thread(
                    target=send_reset_email, args=[email, reset_password_link]
                )
                email_thread.start()
                return redirect('users:forgot_done')
            except User.DoesNotExist:
                return ValueError('bunday emailli user mavjud emas')
        else:
            pass
        return render(request, "register/forgot_password.html", {'form': form})
    
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'register/forgot_password.html', {'form': form})
    
        
class ForgotPasswordDoneView(View):
    def get(self, request):
        return render(request, 'register/forgot_password_done.html', {})
    

class ResetPasswordView(View):
    def post(self, request, uidb64, token):
        user = User.objects.get(id=uidb64)
        if default_token_generator.check_token(user, token):
            form = ResetPasswordForm(data=request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                login(request, user)
                #   bu yerga message yoziladi
                return redirect('users:reset_done')
        else:
            #   bu yerga message yoziladi
            return HttpResponse("tasdiqlash havolasi noto'gri yoki eskirgan")
        return render(request, "register/reset_password.html", {'form': form})
    
    def get(self, request, uidb64, token):
        form = ResetPasswordForm()
        return render(request, 'register/reset_password.html', {'form': form})
    

class ResetPasswordDoneView(View):
    def get(self, request):
        return render(request, 'register/reset_password_done.html', {})
    