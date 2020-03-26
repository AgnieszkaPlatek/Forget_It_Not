from django.contrib import admin

from .models import LearningSession, Question


admin.site.register(LearningSession)
admin.site.register(Question)
