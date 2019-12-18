from django.urls import path
from . import views

#TODO create views
urlpatterns = [
    path('', views.home, name="flashcards-home"),
    path('about/', views.about, name='flashcards-about'),
]