from django.shortcuts import render
from django.views.generic import ListView
from .models import Set, Flashcard
from django.contrib.auth.decorators import login_required


def home(request):
   return render(request, 'flashcards/home.html')


def about(request):
    return render(request, 'flashcards/about.html')


'''@login_required
def set_list(request):
    context = {
        'sets': Set.objects.all()
    }
    return render(request, 'flashcards/set_list.html', context)'''


class SetListView(ListView):
    model = Set
    context_object_name = 'sets'
    ordering = ['-created']

'''@login_required
def flashcard_list(request):
    context = {
        'flashcards': Flashcard.objects.all()
    }
    return render(request, 'flashcards/<str:name>.html', context)'''

class FlashcardListView(ListView):
    model = Flashcard
    template_name = 'flashcards/<str:set>.html'
    context_object_name = 'flashcards'
    ordering = ['added']


@login_required
def learn(request):
    return render(request, 'flashcards/learn.html')


@login_required
def test(request):
    return render(request, 'flashcards/test.html')


