from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views
from .views import (
    SetListView,
    SetCreateView,
    SetUpdateView,
    SetDeleteView,
    FlashcardAddView,
    FlashcardUpdateView,
    FlashcardDeleteView
)


urlpatterns = [
    path('', views.home, name="flashcards-home"),
    path(_('welcome/'), views.welcome, name="flashcards-welcome"),
    path(_('set/list/'), SetListView.as_view(), name="set-list"),
    path(_('set/create/'), SetCreateView.as_view(), name="set-create"),
    path(_('set/<int:pk>/'), views.flashcard_list, name="flashcard-list"),
    path(_('set/<int:pk>/select/'), views.filter_flashcards, name="flashcard-filter"),
    path(_('set/<int:pk>/search/'), views.search_for_flashcards, name="flashcard-search"),
    path(_('set/<int:pk>/update/'), SetUpdateView.as_view(), name="set-update"),
    path(_('set/<int:pk>/delete/'), SetDeleteView.as_view(), name="set-delete"),
    path(_('set/<int:pk>/add/'), FlashcardAddView.as_view(), name="flashcard-add"),
    path(_('set/flashcard/<int:pk>/'), views.flashcard_detail, name="flashcard-detail"),
    path(_('set/flashcard/<int:pk>/update/'), FlashcardUpdateView.as_view(), name="flashcard-update"),
    path(_('set/flashcard/<int:pk>/delete/'), FlashcardDeleteView.as_view(), name="flashcard-delete"),
]

# <app>/<model>_<viewtype>.html - default path for class views
