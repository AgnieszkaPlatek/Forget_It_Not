from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from flashcards.models import Set, Flashcard


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
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
        'total_flashcards': total_flashcards
    }
    return render(request, 'users/profile.html', context)


@login_required
def delete_user(request):
    if request.method == "POST" and "delete" in request.POST:
        request.user.delete()
        messages.success(request, f'Your account has been deleted!')
        return redirect('flashcards-home')
    return render(request, 'users/profile_confirm_delete.html')
