from django.urls import path
from . import views


urlpatterns = [
    path('learn/', views.learn, name="learn"),
    path('set/<int:pk>/learn/', views.learn_set, name="learn-set"),
    path('all/learn/', views.learn_all, name="learn-all"),
    path('learn/question/<int:l_pk>/', views.question, name='learn-question'),
    path('learn/answer/<int:l_pk>/<int:f_pk>/', views.answer, name='learn-answer'),
    path('learn/finished/<int:l_pk>/', views.finished, name="learn-finished"),
]
