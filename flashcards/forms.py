
        from django.forms import ModelForm


from .models import Set, Flashcard


class SetCreateForm(ModelForm):
    class Meta:
        model = Set
        fields = ['name']


class FlashcardAddForm(ModelForm):
    class Meta:
        model = Flashcard
        fields = ['front', 'back']