from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Set(models.Model):
    """
    Set model is a set of flashcards.
    User can create as many sets as he like.
    """
    name = models.CharField(max_length=20, verbose_name=_('name'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    @property
    def count_flashcards(self):
        return Flashcard.objects.filter(set=self).count()

    def get_absolute_url(self):
        return reverse('flashcard-list', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    """
    Flashcard model, each flashcard belongs to one set.
    """
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    front = models.CharField(max_length=50, verbose_name=_('front'))
    back = models.CharField(max_length=50, verbose_name=_('back'))
    added = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('flashcard-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.front} - {self.back}'
