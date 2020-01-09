from django.urls import path
from .views import SetListView, FlashcardListView
from . import views

urlpatterns = [
    path('', views.home, name="flashcards-home"),
    path('about/', views.about, name="flashcards-about"),
    #path('set_list/', views.set_list, name='set-list'),
    path('flashcards/set_list/', SetListView.as_view(), name='set-list'),
    path('flashcards/<str:flashcard.set.name>', FlashcardListView.as_view(), name='flashcard-list'),
    #path('flashcards/<str:name>/', views.flashcard_list, name='flashcard-list'),
    path('learn/', views.learn, name='learn'),
    path('test/', views.test, name='test'),
]

# <app>/<model>_<viewtype>.html - default path for class views