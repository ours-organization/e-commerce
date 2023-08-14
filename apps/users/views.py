from django.shortcuts import render
from django.views.generic import CreateView
from django.views import View

from .models import User
from .forms import RegisterForm


# class RegisterView(View):
    # def post(self, request):
    #     form = RegisterForm(data=request.POST)
    #     if form.is_valid():


class RegisterView(CreateView):
    template_name = 'register/register.html'
    form_class = RegisterForm
