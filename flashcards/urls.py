from django.urls import path
from .views import (
    SetListView,
    FlashcardDetailView
)
from . import views


urlpatterns = [
    path('', views.home, name="flashcards-home"),
    path('about/', views.about, name="flashcards-about"),
    path('set/list/', SetListView.as_view(), name="set-list"),
    path('set/<int:pk>/', views.flashcard_list, name="flashcard-list"),
    path('set/flashcard/<int:pk>/', FlashcardDetailView.as_view(), name="flashcard-detail"),
    path('set/learn/', views.learn, name="learn"),
    path('set/test/', views.test, name="test")
]

# <app>/<model>_<viewtype>.html - default path for class views
