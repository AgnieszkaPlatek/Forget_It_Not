from django.urls import path
from .views import (
    SetListView,
    SetCreateView,
    FlashcardAddView,
    FlashcardDetailView
)
from . import views


urlpatterns = [
    path('', views.home, name="flashcards-home"),
    path('set/list/', SetListView.as_view(), name="set-list"),
    path('set/create/', SetCreateView.as_view(), name="set-create"),
    path('set/<int:pk>/', views.flashcard_list, name="flashcard-list"),
    #path('set/<int:pk>/add/', FlashcardAddView.as_view(), name="flashcard-add"),
    path('set/flashcard/<int:pk>/', FlashcardDetailView.as_view(), name="flashcard-detail"),
    path('set/flashcard/<int:pk>/delete/', views.flashcard_delete, name="flashcard-delete"),
    path('set/learn/', views.learn, name="learn"),
    path('set/test/', views.test, name="test")
]

# <app>/<model>_<viewtype>.html - default path for class views
