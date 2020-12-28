import random

from django.contrib.auth.models import User
from django.db import models

from flashcards.models import Set


class Learn(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    question_ids = models.TextField()
    total_questions = models.IntegerField(null=False, default=0)
    set_to_learn = models.ForeignKey(Set, on_delete=models.CASCADE, null=True)
    learned = models.IntegerField(default=0)

    @property
    def left_to_learn(self):
        return self.total_questions - self.learned

    def make_list_of_questions(self):
        if self.question_ids != '':
            return [int(x) for x in self.question_ids.split(' ')]

    def pick_question(self):
        questions = self.make_list_of_questions()
        question_id = random.choice(questions)
        return question_id

    def mark_learned(self, pk):
        questions = self.make_list_of_questions()
        questions.remove(pk)
        questions_str = [str(x) for x in questions]
        self.question_ids = ' '.join(questions_str)
        self.learned += 1

    @property
    def everything_learned(self):
        return self.learned == self.total_questions

    def __str__(self):
        return f'Learning session {self.pk}'

    def __repr__(self):
        return f'Learn {self.pk}'
