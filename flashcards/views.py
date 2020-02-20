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
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

from .models import Set, Flashcard


def home(request):
    return render(request, 'flashcards/home.html')


class SetListView(LoginRequiredMixin, ListView):
    model = Set
    context_object_name = 'sets'
    ordering = ['-created']


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
    set = get_object_or_404(Set, pk=pk)
    flashcards = Flashcard.objects.filter(set=set)
    context = {
        "set": set,
        "flashcards": flashcards
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


#TODO Fix Foreign Key Issue
class FlashcardAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Flashcard
    fields = ['front', 'back']
    template_name = "flashcards/flashcard_add.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        flashcard = self.get_object()
        if self.request.user == flashcard.owner:
            return True
        return False


#TODO Fix success url
class FlashcardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Flashcard
    #success_url = '/'

    def test_func(self):
        flashcard = self.get_object()
        if self.request.user == flashcard.owner:
            return True
        return False

    # def get_success_url(self):
    #     return reverse('flashcard-list', kwargs={'pk': self.set__pk})


@login_required
def learn(request):
    return render(request, 'flashcards/learn.html')


@login_required
def test(request):
    return render(request, 'flashcards/test.html')

@login_required
def play(request):
    return render(request, 'flashcards/play.html')
