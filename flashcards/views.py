from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Set, Flashcard


def home(request):
    return render(request, 'flashcards/home.html')


def about(request):
    return render(request, 'flashcards/about.html')


class SetListView(ListView):
    model = Set
    context_object_name = 'sets'
    ordering = ['-created']


@login_required
def flashcard_list(request, pk):
    set = get_object_or_404(Set, pk=pk)
    flashcards = Flashcard.objects.filter(set=set)
    context = {
        "set": set,
        "flashcards": flashcards
    }
    return render(request, 'flashcards/flashcard_list.html', context)


class FlashcardDetailView(DetailView):
    model = Flashcard
    context_object_name = 'flashcard'


@login_required
def learn(request):
    return render(request, 'flashcards/learn.html')


@login_required
def test(request):
    return render(request, 'flashcards/test.html')
