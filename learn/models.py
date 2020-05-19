import random

from django.db import models
from django.contrib.auth.models import User

from flashcards.models import Set, Flashcard


class LearningSession(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    set_to_learn = models.ForeignKey(Set, on_delete=models.CASCADE, null=True)
    part_of_set = models.BooleanField(default=False)
    total_questions = models.IntegerField(null=False, default=0)

    @property
    def questions_learned(self):
        return self.total_questions - self.question_set.count()

    @property
    def everything_learned(self):
        return self.question_set.count() == 0

    def pick_question(self):
        questions = Question.objects.filter(session=self)
        question = random.choice(questions)
        return question


    def __str__(self):
        return f'Learning session {self.pk}'


class Question(models.Model):
    session = models.ForeignKey(LearningSession, on_delete=models.CASCADE, null=True)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, unique=False)

    def get_absolute_url(self):
        return reverse('learn-question', kwargs={'l_pk': self.session.id,'f_pk': self.pk})

    def __str__(self):
        return f'Question {self.pk}'
