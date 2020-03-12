from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class FlashcardsQuerySet(models.QuerySet):
    def flashcards_for_set(self, set_pk):
        return self.filter(set=set_pk)


class Set(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def count_flashcards(self):
        return Flashcard.objects.filter(set=self).count()

    def get_absolute_url(self):
        return reverse('flashcard-list', kwargs={'pk': self.pk})


class Flashcard(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    front = models.CharField(max_length=50)
    back = models.CharField(max_length=50)
    added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = FlashcardsQuerySet.as_manager()

    def __str__(self):
        return f'{self.front} - {self.back}'

    def get_absolute_url(self):
        return reverse('flashcard-detail', kwargs={'pk': self.pk})
