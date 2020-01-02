from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="flashcards-home"),
    path('about/', views.about, name="flashcards-about"),
    path('set_list/', views.set_list, name='set-list'),
    path('learn/', views.learn, name='learn'),
    path('learn-congrats/', views.learn_congrats, name='learn-congrats'),
    path('test/', views.test, name='test'),
    path('test_congrats/', views.test_congrats, name='test-congrats'),
]