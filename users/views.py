from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from flashcards.models import Set, Flashcard
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .tokens import account_activation_token


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if request.LANGUAGE_CODE == 'en-us':
            email_path = 'users/account_activation_email.html'
        else:
            email_path = 'users/email_aktywacyjny.html'
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = _('Confirm Your Forget-It-Not Account')
            message = render_to_string(email_path,
                                       {'user': user,
                                        'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user),
                                        })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            msg = _('Please confirm your email to complete registration.')
            messages.success(request, msg)

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'register': 'active'})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        msg = _('Your account has been confirmed. You can log in.')
        messages.success(request, msg)
        return redirect('login')
    else:
        msg = _('The confirmation link is invalid!')
        messages.warning(request, msg)
        return redirect('home')


@login_required
def profile(request):
    username = request.user.username
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            msg = _('Your account has been updated!')
            messages.success(request, msg)
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    total_sets = Set.objects.filter(owner=request.user).count()
    total_flashcards = Flashcard.objects.filter(owner=request.user).count()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'total_sets': total_sets,
        'total_flashcards': total_flashcards,
        'title': f'{username} - profile',
        'profile': 'active'
    }

    if request.user.username == 'demo':
        context['demo'] = True
    return render(request, 'users/profile.html', context)


@login_required
def delete_user(request):
    if request.method == 'POST' and 'delete' in request.POST:
        request.user.delete()
        msg = _('Your account has been deleted!')
        messages.success(request, msg)
        return redirect('flashcards-home')
    return render(request, 'users/profile_confirm_delete.html')
