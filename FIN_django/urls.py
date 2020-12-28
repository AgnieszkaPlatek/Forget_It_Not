"""FIN_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from users import views as user_views


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path(_('register/'), user_views.register, name='register'),
    path('activate/<uidb64>/<token>/', user_views.activate, name='activate'),
    path(_('profile/'), user_views.profile, name='profile'),
    path(_('login/'), LoginView.as_view(template_name='users/login.html', extra_context={'log_in': 'active'}),
         name='login'),
    path(_('logout/'), LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path(_('delete_confirm/'), user_views.delete_user, name='delete'),
    path(_('password-reset/'),
         PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path(_('password-reset-confirm/<uidb64>/<token>/'),
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path(_('password-reset/done/'),
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path(_('password-reset-complete/'),
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', include('flashcards.urls')),
    path('', include('learn.urls'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
