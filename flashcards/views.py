from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy

from .models import Set, Flashcard


def home(request):
    if request.user.is_authenticated:
        return render(request, 'flashcards/home.html')
    else:
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
    flashcards = Flashcard.objects.flashcards_for_set(set.pk)
    page = request.GET.get('page', 1)
    paginator = Paginator(flashcards, 30)
    try:
        flashcards = paginator.page(page)
    except PageNotAnInteger:
        flashcards = paginator.page(1)
    except EmptyPage:
        flashcards = paginator.page(paginator.num_pages)
    count = set.flashcard_set.count()
    context = {
        "set": set,
        "flashcards": flashcards,
        "count": count
    }
    return render(request, 'flashcards/flashcard_list.html', context)


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
