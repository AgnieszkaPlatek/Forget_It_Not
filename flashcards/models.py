from django.db import models
from django.contrib.auth.models import User


class Set(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    front = models.CharField(max_length=50)
    back = models.CharField(max_length=50)
    added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.front} - {self.back}'