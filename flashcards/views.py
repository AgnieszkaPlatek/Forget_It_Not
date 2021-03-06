from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from FIN_django.helpers import make_list_of_ids, make_question_ids, create_example_set, search
from FIN_django.settings import guest_password, FLASHCARDS_PER_PAGE
from learn.models import Learn
from .models import Set, Flashcard


def home(request):
    if not request.user.is_authenticated:
        return redirect('flashcards-welcome')
    else:
        total_sets = Set.objects.filter(owner=request.user).count()
        flashcards = Flashcard.objects.filter(owner=request.user)
        query = request.GET.get('search')
        context = {'total_sets': total_sets, 'total_flashcards': flashcards.count()}
        if query and len(query) > 2:
            context['flashcards'] = search(query, flashcards)
        return render(request, 'flashcards/home.html', context)


def welcome(request):
    if request.method == 'POST' and 'demo' in request.POST:
        user = authenticate(username='demo', password=guest_password)
        if user:
            pk = user.pk

            # Delete all previously created demo sets with the exception of example set
            Set.objects.filter(owner=pk).exclude(name='example').delete()

            # Delete all previously created flashcards added by demo user to the example set
            try:
                example_set = Set.objects.get(owner=pk, name='example')
                flashcards_to_be_deleted = Flashcard.objects.filter(set=example_set)[5:]
                for f in flashcards_to_be_deleted:
                    f.delete()
                login(request, user)
            except Set.DoesNotExist:
                create_example_set(user)

        else:
            # Create guest active demo user.
            user = User.objects.create_user(username='demo', password=guest_password)
            user.is_active = True
            user.save()

            # Create example set with few example flashcards.
            create_example_set(user)
            authenticate(username='demo', password=guest_password)

        return redirect('flashcards-home')
    return render(request, 'flashcards/welcome.html')


class SetListView(LoginRequiredMixin, ListView):
    model = Set
    context_object_name = 'sets'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(SetListView, self).get_context_data(**kwargs)
        context['set_list'] = 'active'
        return context


class SetCreateView(LoginRequiredMixin, CreateView):
    model = Set
    fields = ['name']
    template_name = 'flashcards/set_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Set
    fields = ['name']
    template_name = 'flashcards/set_update.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        set = self.get_object()
        return self.request.user == set.owner


class SetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Set
    success_url = reverse_lazy('set-list')

    def test_func(self):
        set = self.get_object()
        return self.request.user == set.owner


@login_required
def flashcard_list(request, pk):
    set = get_object_or_404(Set, pk=pk, owner=request.user)
    flashcards = set.flashcard_set.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(flashcards, FLASHCARDS_PER_PAGE)
    try:
        flashcards = paginator.page(page)
    except PageNotAnInteger:
        flashcards = paginator.page(1)
    except EmptyPage:
        flashcards = paginator.page(paginator.num_pages)
    context = {'set': set, 'flashcards': flashcards, 'count': set.count_flashcards, 'title': str(set.name)}

    return render(request, 'flashcards/flashcard_list.html', context)


def filter_flashcards(request, pk):
    set = get_object_or_404(Set, pk=pk, owner=request.user)
    flashcards = Flashcard.objects.filter(set=set).order_by('added')
    min_date = request.GET.get('min_date')
    max_date = request.GET.get('max_date')
    context = {'set': set}
    if min_date:
        flashcards = flashcards.filter(added__gte=min_date)
        context['flashcards'] = flashcards
    if max_date:
        flashcards = flashcards.filter(added__lte=max_date)
        context['flashcards'] = flashcards
    if request.method == 'POST' and 'learn' in request.POST:
        question_ids = make_question_ids(flashcards)
        session = Learn.objects.create(learner=request.user, question_ids=question_ids,
                                       total_questions=len(flashcards), set_to_learn=set)
        return redirect('learn-part', l_pk=session.pk)

    return render(request, 'flashcards/flashcards_select_form.html', context)


def search_for_flashcards(request, pk):
    set = get_object_or_404(Set, pk=pk, owner=request.user)
    flashcards = Flashcard.objects.filter(set=set)
    query = request.GET.get('search')
    context = {'set': set}
    if query and len(query) > 2:
        context['flashcards'] = search(query, flashcards)
    return render(request, 'flashcards/flashcards_search.html', context)


def find_next_flashcard(pk):
    """
    pk: the primary key of a flashcard

    returns: the primary key of the next flashcards in the set
    """
    flashcards_ids = make_list_of_ids(pk)
    index = flashcards_ids.index(pk)
    try:
        return flashcards_ids[index + 1]
    except IndexError:
        return None


def find_previous_flashcard(pk):
    """
    pk: the primary key of a flashcard

    returns: the primary key of the previous flashcards in the set
    """
    flashcards_ids = make_list_of_ids(pk)
    index = flashcards_ids.index(pk)
    if flashcards_ids[0] == pk:
        return None
    return flashcards_ids[index - 1]


@login_required
def flashcard_detail(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    next_id = find_next_flashcard(pk)
    previous_id = find_previous_flashcard(pk)
    context = {'flashcard': flashcard}
    if next_id:
        context['next_id'] = next_id
    if previous_id:
        context['previous_id'] = previous_id
    return render(request, 'flashcards/flashcard_detail.html', context)


class FlashcardAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Flashcard
    context_object_name = 'flashcard'
    fields = ['front', 'back']
    template_name = 'flashcards/flashcard_add.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pk = self.kwargs.get('pk', None)
        form.instance.set = get_object_or_404(Set, pk=pk)
        return super().form_valid(form)

    def test_func(self):
        pk = self.kwargs.get('pk', None)
        set = get_object_or_404(Set, pk=pk)
        return self.request.user == set.owner


class FlashcardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Flashcard
    context_object_name = 'flashcard'
    fields = ['front', 'back']
    template_name = 'flashcards/flashcard_update.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pk = self.kwargs.get('pk', None)
        flashcard = get_object_or_404(Flashcard, pk=pk)
        form.instance.set = flashcard.set
        return super().form_valid(form)

    def test_func(self):
        flashcard = self.get_object()
        return self.request.user == flashcard.owner


class FlashcardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Flashcard

    def test_func(self):
        flashcard = self.get_object()
        return self.request.user == flashcard.owner

    def get_success_url(self):
        flashcard = self.get_object()
        return reverse_lazy('flashcard-list', kwargs={'pk': flashcard.set.pk})
