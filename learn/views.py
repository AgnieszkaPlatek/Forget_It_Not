from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from flashcards.models import Set, Flashcard
from .models import LearningSession, Question


@login_required
def learn(request):
    user = request.user
    user_sets = Set.objects.filter(owner=user)
    sets = []
    for set in user_sets:
        if set.count_flashcards > 0:
            sets.append(set)
    empty = user.flashcard_set.count() == 0
    return render(request, 'learn/learn.html', {"sets": sets, "empty": empty})


@login_required
def learn_set(request, pk):
    LearningSession.objects.all().delete()
    set = get_object_or_404(Set, pk=pk)
    total = set.count_flashcards
    session = LearningSession(learner=request.user, set_to_learn=set, total_questions=total)
    session.save()
    l_pk = session.pk
    for flashcard in set.flashcard_set.all():
        q = Question(session=session, flashcard=flashcard)
        q.save()
    context = {"set": set, "total": total, "l_pk": l_pk}
    return render(request, 'learn/learn_set.html', context)


def learn_part(request, l_pk):
    session = get_object_or_404(LearningSession, pk=l_pk)
    set = session.set_to_learn
    l_pk = session.pk
    total = session.total_questions
    context = {"set": set, "total": total, "l_pk": l_pk}
    return render(request, 'learn/learn_part.html', context)


@login_required
def learn_all(request):
    LearningSession.objects.all().delete()
    user = request.user
    flashcards = Flashcard.objects.filter(owner=user)
    total = flashcards.objects.count()
    session = LearningSession(learner=user, total_questions=total)
    session.save()
    for flashcard in flashcards:
        q = Question(session=session, flashcard=flashcard)
        q.save()
    l_pk = session.pk
    context = {"total": total, "l_pk": l_pk}
    return render(request, 'learn/learn_all.html', context)


@login_required
def question(request, l_pk):
    session = get_object_or_404(LearningSession, pk=l_pk)
    question = session.pick_question()
    if session.set_to_learn:
        set = session.set_to_learn
    else:
        set = None
    front = question.flashcard.front
    total = session.total_questions
    count = session.questions_learned
    f_pk = question.pk
    context = {"set": set, "l_pk": l_pk, "f_pk": f_pk, "front": front, "count": count,
               "total": total}
    return render(request, 'learn/question.html', context)


@login_required
def answer(request, l_pk, f_pk):
    session = get_object_or_404(LearningSession, pk=l_pk)
    question = get_object_or_404(Question, pk=f_pk)
    if session.set_to_learn:
        set = session.set_to_learn
    else:
        set = None
    back = question.flashcard.back
    total = session.total_questions
    count = session.questions_learned
    finished = session.everything_learned
    context = {"set": set, "l_pk": l_pk, "f_pk": f_pk, "count": count, "back": back,
               "total": total, "finished": finished}

    if request.method == "POST" and "learned" in request.POST:
        # Delete the learned question object.
        # Check if there are more flashcards to learn.
        if session.question_set.count() > 1:
            question.delete()
            return redirect('learn-question', l_pk=l_pk)
        else:
            # CHeck if user is learning one set or all flashcards.
            if session.set_to_learn:
                return redirect('learn-finished', l_pk=l_pk)
            else:
                return redirect('learn-finished', l_pk=l_pk)

    elif request.method == "POST" and "not-learned" in request.POST:
        return redirect('learn-question', l_pk=l_pk)

    return render(request, 'learn/answer.html', context)


@login_required
def finished(request, l_pk):
    session = get_object_or_404(LearningSession, pk=l_pk)
    if session.set_to_learn:
        set = session.set_to_learn
    else:
        set = None
    total = session.total_questions
    context = {"total": total, "set": set}
    return render(request, 'learn/finished.html', context)
