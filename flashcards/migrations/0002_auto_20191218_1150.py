# Generated by Django 3.0 on 2019-12-18 10:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Flashcards_set',
            new_name='Set',
        ),
        migrations.RenameField(
            model_name='flashcard',
            old_name='flashcards_set',
            new_name='set',
        ),
    ]
