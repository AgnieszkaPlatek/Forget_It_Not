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


class SetListView(ListView):
    model = Set
    context_object_name = 'sets'
    ordering = ['-created']


class SetCreateView(CreateView):
    model = Set
    fields = ['name']
    template_name = "flashcards/set_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class FlashcardAddView(CreateView):
    model = Flashcard
    fields = ['front', 'back']
    template_name = "flashcards/flashcard_add.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.set.id = self.request.set_id
        return super().form_valid(form)



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
def flashcard_delete(request, pk):
    return render(request, 'flashcards/flashcard_delete.html')


@login_required
def learn(request):
    return render(request, 'flashcards/learn.html')


@login_required
def test(request):
    return render(request, 'flashcards/test.html')
