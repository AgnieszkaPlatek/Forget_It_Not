from django.urls import path
from . import views


urlpatterns = [
    path('learn/', views.learn, name="learn"),
    # path('learn-all/', views.learn_all, name="learn-all"),
    # path('set/<int:pk>/learn', views.learn_set, name="learn-set"),
    path('set/learn/question/<int:pk>/', views.question, name='learn-question'),
    path('set/learn/answer/<int:pk>/', views.answer, name='learn-answer'),
    path('set/<int:pk>/learn/finished/', views.learn_finished, name='learn-finished')
]