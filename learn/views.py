from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from flashcards.models import Set, Flashcard



@login_required
def question(request, pk):
    owner = request.user
    flashcard = get_object_or_404(Flashcard, pk=pk, owner=owner)
    set = flashcard.set
    context = {
        "flashcard": flashcard,
        "set": set
    }
    return render(request, 'learn/question.html', context)


@login_required
def answer(request, pk):
    owner = request.user
    flashcard = get_object_or_404(Flashcard, pk=pk, owner=owner)
    set = flashcard.set
    context = {
        "flashcard": flashcard,
        "set": set
    }
    return render(request, 'learn/answer.html', context)


@login_required
def learn_finished(request, pk):
    owner = request.user
    set = get_object_or_404(Set, pk=pk, owner=owner)
    context = {
        "set": set,
    }
    return render(request, 'learn/learning_finished.html', context)


# @login_required
# def learn_all(request):
#     sets = Set.objects.filter(owner=request.user)
#     flashcards = Flashcard.objects.filter(owner=request.user)
#     context = {
#         "flashcards": flashcards
#     }
#     return render(request, 'flashcards/learn.html', context)
#


@login_required
def learn(request):
    sets = Set.objects.filter(owner=request.user)
    return render(request, 'learn/learn.html', {"sets":sets})
