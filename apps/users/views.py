import datetime

from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse

from .models import User
from .forms import RegisterForm, CodeVerifyForm
from apps.common.utility import send_mail



class HomePageView(TemplateView):
    template_name = 'base.html'


class RegisterView(View):
    def post(self, request):
        form = RegisterForm(data=request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('users:code')
        else:
            pass
        return render(request, 'register/register.html', {'form': form})
    
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register/register.html', {'form': form})
    

class CodeVerifyView(View):
    def post(self, request):
        form = CodeVerifyForm(data=request.POST)
        code = self.request.POST['code']
        user = self.request.user

        if self.request.user.is_authenticated:
            if form.is_valid():
                code_instance = form.save(commit=False)
                code_instance.code = code
                code_instance.user = self.request.user
                code_instance.save()
                self.check_verify(user, code_instance)
                return HttpResponse('success!!!!!')
            else:
                return HttpResponse('Form is not valid')
        else:
            return redirect('users:register')

    # def post(self, request, token):
    #     user_id, code = verify_verification_token(token)
    #     print(f'request user: {request.user}')
    #     if user_id is not None and code is not None:
    #         try:
    #             self.check_verify(user_id, code)
    #             return HttpResponse("tasdiqlash ko'di to'g'ri")
    #         except:
    #             return HttpResponse("tasdiqlash ko'di xato yoki eskirgan")
    #     else:
    #         return HttpResponse('User mavjud emas')


    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.datetime.now(), code=code, is_confirmed=False)
        print(f"verifies = {verifies}")
        if not verifies.exists():
            return HttpResponse('xato verify code')
        verifies.update(is_confirmed=True)

        if user.auth_step == User.AuthStep.FIRST_STEP:
            user.auth_step = User.AuthStep.SECOND_STEP
            user.save()
        return True
    
    def get(self, request):
        print('64 line get worked')
        form = CodeVerifyForm()
        return render(request, 'register/codeverify.html', {'form': form})
    