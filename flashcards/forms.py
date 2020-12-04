from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Set, Flashcard


class SetCreateForm(ModelForm):
    class Meta:
        model = Set
        fields = ['name']

class FlashcardAddForm(ModelForm):
    class Meta:
        model = Flashcard
        fields = ['front', 'back']
