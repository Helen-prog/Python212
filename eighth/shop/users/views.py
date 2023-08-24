from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .models import EmailVerification, User
from products.models import Basket


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active and user.is_verify_email:
                auth.login(request, user)
                return redirect('index')
    else:
        form = UserLoginForm()
    context = {
        "title": "Авторизация",
        "form": form
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():

            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # subject = 'Ваш аккаунт создан'
            # message = username + "! Добро пожаловать в Store!"
            # print(form.cleaned_data)
            # try:
            #     send_mail(
            #         subject,
            #         message,
            #         settings.EMAIL_HOST_USER,
            #         [email]
            #     )
            # except BadHeaderError:
            #     return HttpResponse('Обнаружен неверный заголовок')

            form.save()
            messages.success(request, 'Подтвердите регистрацию по почте')  # Вы успешно зарегистрировались!
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        "title": "Регистрация",
        'form': form
    }
    return render(request, 'users/register.html', context)


def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    context = {
        'title': 'Профиль пользователя',
        'form': form,
        'baskets': Basket.objects.filter(user=user)
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')


class EmailVerificationView(TemplateView):
    template_name = 'users/email_verification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "StoreShop - Подвтверждение электронной почты"
        return context

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verify_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect('index')

