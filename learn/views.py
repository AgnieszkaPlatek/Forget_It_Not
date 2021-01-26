from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from FIN_django.helpers import make_question_ids
from flashcards.models import Set, Flashcard
from .models import Learn


@login_required
def learn(request):
    user = request.user
    user_sets = Set.objects.filter(owner=user)
    sets = []
    for set in user_sets:
        if set.count_flashcards > 0:
            sets.append(set)
    empty = user.flashcard_set.count() == 0
    num_flashcards = Flashcard.objects.filter(owner=user).count
    context = {'sets': sets, 'empty': empty, 'num_sets': len(sets), 'num_flashcards': num_flashcards,
               'learn': 'active', 'title': 'Learn'}
    return render(request, 'learn/learn.html', context)


@login_required
def learn_set(request, pk):
    set = get_object_or_404(Set, pk=pk)
    question_ids = make_question_ids(set.flashcard_set.all())
    total = set.flashcard_set.count()
    session = Learn.objects.create(learner=request.user, question_ids=question_ids, total_questions=total,
                                    set_to_learn=set)
    context = {'set': set, 'total': total, 'l_pk': session.pk, 'title': f'Learn {set.name}'}
    return render(request, 'learn/learn_intro.html', context)


def learn_part(request, l_pk):
    session = get_object_or_404(Learn, pk=l_pk)
    context = {'set': session.set_to_learn, 'total': session.total_questions, 'l_pk': session.pk, 'part': True}
    return render(request, 'learn/learn_intro.html', context)


@login_required
def learn_all(request):
    user = request.user
    flashcards = Flashcard.objects.filter(owner=user)
    question_ids = make_question_ids(flashcards)
    session = Learn.objects.create(learner=user, question_ids=question_ids, total_questions=len(flashcards))
    context = {'total': len(flashcards), 'l_pk': session.pk, 'title': 'Learn all flashcards'}
    return render(request, 'learn/learn_intro.html', context)


@login_required
def question(request, l_pk):
    session = get_object_or_404(Learn, pk=l_pk)
    question_id = session.pick_question()
    flashcard = get_object_or_404(Flashcard, pk=question_id)
    context = {'set': set, 'l_pk': l_pk, 'f_pk': question_id, 'front': flashcard.front, 'learned': session.learned,
               'total': session.total_questions}
    if session.set_to_learn:
        context['set'] = session.set_to_learn
    return render(request, 'learn/question.html', context)


@login_required
def answer(request, l_pk, f_pk):
    session = get_object_or_404(Learn, pk=l_pk)
    flashcard = get_object_or_404(Flashcard, pk=f_pk)

    if request.method == 'POST' and 'learned' in request.POST:
        session.mark_learned(f_pk)
        session.save()
        # Check if there are more flashcards to learn.
        if session.left_to_learn > 0:
            return redirect('learn-question', l_pk=l_pk)
        else:
            return redirect('learn-finished', l_pk=l_pk)

    elif request.method == 'POST' and 'not-learned' in request.POST:
        return redirect('learn-question', l_pk=l_pk)

    context = {'set': set, 'l_pk': l_pk, 'f_pk': f_pk, 'learned': session.learned, 'back': flashcard.back,
               'total': session.total_questions}
    if session.set_to_learn:
        context['set'] = session.set_to_learn
    return render(request, 'learn/answer.html', context)


@login_required
def finished_learning(request, l_pk):
    session = get_object_or_404(Learn, pk=l_pk)
    if session.set_to_learn:
        set = session.set_to_learn
    else:
        set = None
    context = {'total': session.total_questions, 'set': set}
    return render(request, 'learn/finished.html', context)
