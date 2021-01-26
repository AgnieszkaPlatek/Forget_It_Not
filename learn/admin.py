from django.contrib import admin

from .models import Learn


@admin.register(Learn)
class LearnAdmin(admin.ModelAdmin):
    model = Learn
    list_display = ('id', 'learner', 'total_questions')
