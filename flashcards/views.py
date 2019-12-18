from django.shortcuts import render


def home(request):
    return render(request, 'flashcards/home.html')

def about(request):
    return render(request, 'flashcards/about.html')

