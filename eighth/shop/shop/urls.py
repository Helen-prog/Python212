"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('users/', include('users.urls')),

    path("reset-password/", auth_views.PasswordResetView.as_view(template_name="users/reset_password.html"),
         name='reset_password'),
    # пользователь отправляет письмо для сброса
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password_sent.html'),
         name='password_reset_done'),
    # сообщение отправленное по электронной почте
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/reset.html'),
         name="password_reset_confirm"),
    #  электронное письмо со ссылкой и инструкциями по сбросу
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password_complete.html'), name='password_reset_complete'),
    # сообщение об успешном сбросе пароля
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

