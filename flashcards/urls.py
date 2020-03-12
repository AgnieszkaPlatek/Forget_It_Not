from django.urls import path
from .views import (
    SetListView,
    SetCreateView,
    SetUpdateView,
    SetDeleteView,
    FlashcardAddView,
    FlashcardDetailView,
    FlashcardUpdateView,
    FlashcardDeleteView
)
from . import views


urlpatterns = [
    path('', views.home, name="flashcards-home"),
    path('set/list/', views.set_list, name="set-list"),
    path('set/create/', SetCreateView.as_view(), name="set-create"),
    path('set/<int:pk>/', views.flashcard_list, name="flashcard-list"),
    path('set/<int:pk>/update/', SetUpdateView.as_view(), name="set-update"),
    path('set/<int:pk>/delete/', SetDeleteView.as_view(), name="set-delete"),
    path('set/<int:pk>/add/', FlashcardAddView.as_view(), name="flashcard-add"),
    path('set/flashcard/<int:pk>/', FlashcardDetailView.as_view(), name="flashcard-detail"),
    path('set/flashcard/<int:pk>/update/', FlashcardUpdateView.as_view(), name="flashcard-update"),
    path('set/flashcard/<int:pk>/delete/', FlashcardDeleteView.as_view(), name="flashcard-delete"),
]

# <app>/<model>_<viewtype>.html - default path for class views
