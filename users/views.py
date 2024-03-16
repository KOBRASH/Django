import random
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth import logout, get_user_model
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.forms import UserRegisterForm, UserProfileForm, UserPasswordResetForm
from users.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages


class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('catalog:home')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Получаем пользователя, но пока не сохраняем его в базу данных
        user = form.save(commit=False)

        # Устанавливаем флаг is_active в False, чтобы пользователь был неактивным до верификации
        user.is_active = False

        # Сохраняем пользователя в базе данных
        user.save()

        # Генерируем уникальный токен для пользователя
        token = default_token_generator.make_token(user)

        # Генерируем ссылку для верификации
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = reverse('users:verify_email', kwargs={'uidb64': uid, 'token': token})

        # Отправляем письмо с кодом верификации
        subject = 'Подтвердите ваш адрес электронной почты'
        message = render_to_string('users/verification_email.html', {
            'user': user,
            'verification_url': verification_url,
            'site_name': 'Django'
        })
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль!',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:home'))



class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'users/user_form'
    success_url = reverse_lazy('users:login')


User = get_user_model()

class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/email_verified.html')
        else:
            messages.error(request, 'Ссылка для подтверждения адреса электронной почты недействительна.')
            return redirect(reverse_lazy('users:register'))
