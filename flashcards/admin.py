from django.contrib import admin

from .models import Flashcard, Set


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    model = Set
    list_display = ('id', 'name', 'owner', 'created')
    list_filter = ('owner', 'created')
    search_fields = ('name', 'owner')


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    model = Flashcard
    list_display = ('id', '__str__', 'owner', 'set', 'added')
    list_filter = ('set', 'owner', 'added')
    search_fields = ('front', 'back', 'set', 'owner')
