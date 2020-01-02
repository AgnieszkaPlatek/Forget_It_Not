from django.shortcuts import render
from .models import Set, Flashcard
from django.contrib.auth.decorators import login_required


def home(request):
   return render(request, 'flashcards/home.html')


def about(request):
    return render(request, 'flashcards/about.html')


@login_required
def set_list(request):
    context = {
        'sets': Set.objects.all()
    }
    return render(request, 'flashcards/set_list.html', context)


@login_required
def learn(request):
    return render(request, 'flashcards/learn.html')


@login_required
def test(request):
    return render(request, 'flashcards/test.html')


@login_required
def learn_congrats(request):
    return render(request, 'flashcards/learn_congrats.html')


@login_required
def test_congrats(request):
    return render(request, 'flashcards/test_congrats.html')

