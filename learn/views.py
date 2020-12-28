from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

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
    num_sets = len(sets)
    num_flashcards = Flashcard.objects.filter(owner=user).count
    context = {"sets": sets, "empty": empty, "num_sets": num_sets, "num_flashcards": num_flashcards,
               "learn": "active", "title": "Learn"}
    return render(request, 'learn/learn.html', context)


def make_question_ids(flashcards):
    question_ids = [flashcard.pk for flashcard in flashcards]
    question_str_ids = [str(id) for id in question_ids]
    return ' '.join(question_str_ids)


@login_required
def learn_set(request, pk):
    set = get_object_or_404(Set, pk=pk)
    question_ids = make_question_ids(set.flashcard_set.all())
    total = set.flashcard_set.count()
    session = Learn(learner=request.user, question_ids=question_ids, total_questions=total, set_to_learn=set)
    session.save()
    l_pk = session.pk
    context = {"set": set, "total": total, "l_pk": l_pk, "title": f"Learn {set.name}"}
    return render(request, 'learn/learn_intro.html', context)


def learn_part(request, l_pk):
    session = get_object_or_404(Learn, pk=l_pk)
    set = session.set_to_learn
    l_pk = session.pk
    total = session.total_questions
    part = True
    context = {"set": set, "total": total, "l_pk": l_pk, "part": part}
    return render(request, 'learn/learn_intro.html', context)


@login_required
def learn_all(request):
    user = request.user
    flashcards = Flashcard.objects.filter(owner=user)
    question_ids = make_question_ids(flashcards)
    total = len(flashcards)
    session = Learn(learner=user, question_ids=question_ids, total_questions=total)
    session.save()
    l_pk = session.pk
    context = {"total": total, "l_pk": l_pk, "title": "Learn all flashcards"}
    return render(request, 'learn/learn_intro.html', context)


@login_required
def question(request, l_pk):
    session = get_object_or_404(Learn, pk=l_pk)
    question_id = session.pick_question()
    flashcard = get_object_or_404(Flashcard, pk=question_id)
    front = flashcard.front
    total = session.total_questions
    learned = session.learned
    context = {"set": set, "l_pk": l_pk, "f_pk": question_id, "front": front, "learned": learned,
               "total": total}
    if session.set_to_learn:
        context["set"] = session.set_to_learn
    return render(request, 'learn/question.html', context)


@login_required
def answer(request, l_pk, f_pk):
    session = get_object_or_404(Learn, pk=l_pk)
    flashcard = get_object_or_404(Flashcard, pk=f_pk)

    if request.method == "POST" and "learned" in request.POST:
        session.mark_learned(f_pk)
        session.save()
        # Check if there are more flashcards to learn.
        if session.left_to_learn > 0:
            return redirect('learn-question', l_pk=l_pk)
        else:
            return redirect('learn-finished', l_pk=l_pk)

    elif request.method == "POST" and "not-learned" in request.POST:
        return redirect('learn-question', l_pk=l_pk)

    back = flashcard.back
    total = session.total_questions
    learned = session.learned
    context = {"set": set, "l_pk": l_pk, "f_pk": f_pk, "learned": learned, "back": back, "total": total}
    if session.set_to_learn:
        context["set"] = session.set_to_learn
    return render(request, 'learn/answer.html', context)


@login_required
def finished_learning(request, l_pk):
    session = get_object_or_404(Learn, pk=l_pk)
    if session.set_to_learn:
        set = session.set_to_learn
    else:
        set = None
    total = session.total_questions
    context = {"total": total, "set": set}
    return render(request, 'learn/finished.html', context)
