from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse_lazy



from .models import Set, Flashcard
from learn.models import LearningSession, Question



def is_valid_query(p):
    return p != '' and p is not None

def home(request):
    if request.user.is_authenticated:
        total_sets = Set.objects.filter(owner=request.user).count()
        total_flashcards = Flashcard.objects.filter(owner=request.user).count()
        flashcards = Flashcard.objects.filter(owner=request.user)
        query = request.GET.get('search')
        context = {'total_sets': total_sets, 'total_flashcards': total_flashcards}
        if is_valid_query(query):
            flashcards = flashcards.filter(
                Q(front__icontains=query) |
                Q(back__icontains=query)).distinct()
            context['flashcards'] = flashcards
        return render(request, 'flashcards/home.html', context)
    else:
        return redirect('flashcards-welcome')


def welcome(request):
    if request.method == "POST" and "demo" in request.POST:
        user = authenticate(username="guest", password="testing321")
        if user is not None:
            login(request, user)
            return redirect('flashcards-home')
    return render(request, 'flashcards/welcome.html')


class SetListView(LoginRequiredMixin, ListView):
    model = Set
    context_object_name = 'sets'
    ordering = ['-created']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class SetCreateView(LoginRequiredMixin, CreateView):
    model = Set
    fields = ['name']
    template_name = "flashcards/set_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Set
    fields = ['name']
    template_name = "flashcards/set_update.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        set = self.get_object()
        if self.request.user == set.owner:
            return True
        return False


class SetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Set
    success_url = '/set/list/'

    def test_func(self):
        set = self.get_object()
        if self.request.user == set.owner:
            return True
        return False


@login_required
def flashcard_list(request, pk):
    set = get_object_or_404(Set, pk=pk, owner=request.user)
    flashcards = set.flashcard_set.order_by('added')
    page = request.GET.get('page', 1)
    paginator = Paginator(flashcards, 30)
    try:
        flashcards = paginator.page(page)
    except PageNotAnInteger:
        flashcards = paginator.page(1)
    except EmptyPage:
        flashcards = paginator.page(paginator.num_pages)
    count = set.count_flashcards
    query = request.GET.get('search')
    qs = set.flashcard_set.order_by('added')
    context = {
        "set": set,
        "flashcards": flashcards,
        "count": count,
    }
    if is_valid_query(query):
        qs = qs.filter(
            Q(front__icontains=query) |
            Q(back__icontains=query)).distinct()
        context["qs"] = qs
        del context["flashcards"]

    return render(request, 'flashcards/flashcard_list.html', context)


def filter_flashcards(request, pk):
    set = get_object_or_404(Set, pk=pk, owner=request.user)
    flashcards = Flashcard.objects.filter(set=set).order_by('added')
    min_date = request.GET.get('min_date')
    max_date = request.GET.get('max_date')
    context = {"set": set}
    if is_valid_query(min_date):
        flashcards = flashcards.filter(added__gte=min_date)
        context['flashcards'] = flashcards
    if is_valid_query(max_date):
        flashcards = flashcards.filter(added__lte=max_date)
        context['flashcards'] = flashcards
    if request.method == "POST" and "learn" in request.POST:
        LearningSession.objects.all().delete()
        total = len(flashcards)
        session = LearningSession(learner=request.user, set_to_learn=set, total_questions=total)
        session.save()
        for flashcard in flashcards:
            q = Question(session=session, flashcard=flashcard)
            q.save()
        l_pk = session.pk
        return redirect('learn-part', l_pk=l_pk)

    return render(request, 'flashcards/flashcards_select_form.html', context)


def search_for_flashcards(request, pk):
    set = get_object_or_404(Set, pk=pk, owner=request.user)
    flashcards = Flashcard.objects.filter(set=set).order_by('added')
    query = request.GET.get('search')
    context = {
        "set": set
    }
    if is_valid_query(query):
        flashcards = flashcards.filter(
            Q(front__icontains=query) |
            Q(back__icontains=query)).distinct()
        context['flashcards'] = flashcards
    return render(request, 'flashcards/flashcards_search.html', context)


class FlashcardDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Flashcard
    context_object_name = 'flashcard'

    def test_func(self):
        set = self.get_object()
        if self.request.user == set.owner:
            return True
        return False


class FlashcardAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Flashcard
    context_object_name = 'flashcard'
    fields = ['front', 'back']
    template_name = "flashcards/flashcard_add.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pk = self.kwargs.get("pk", None)
        form.instance.set = get_object_or_404(Set, pk=pk)
        return super().form_valid(form)

    def test_func(self):
        pk = self.kwargs.get("pk", None)
        set = get_object_or_404(Set, pk=pk)
        if self.request.user == set.owner:
            return True
        return False


class FlashcardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Flashcard
    context_object_name = 'flashcard'
    fields = ['front', 'back']
    template_name = "flashcards/flashcard_update.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pk = self.kwargs.get("pk", None)
        flashcard = get_object_or_404(Flashcard, pk=pk)
        form.instance.set = flashcard.set
        return super().form_valid(form)

    def test_func(self):
        flashcard = self.get_object()
        if self.request.user == flashcard.owner:
            return True
        return False


class FlashcardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Flashcard

    def test_func(self):
        flashcard = self.get_object()
        if self.request.user == flashcard.owner:
            return True
        return False

    def get_success_url(self):
        flashcard = self.get_object()
        pk = flashcard.set.pk
        return reverse_lazy('flashcard-list', kwargs={'pk': pk})
