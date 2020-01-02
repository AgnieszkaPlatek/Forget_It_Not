# Generated by Django 3.0 on 2019-12-22 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0002_auto_20191218_1150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flashcard',
            old_name='date_added',
            new_name='added',
        ),
        migrations.RenameField(
            model_name='flashcard',
            old_name='answer',
            new_name='back',
        ),
        migrations.RenameField(
            model_name='flashcard',
            old_name='question',
            new_name='front',
        ),
        migrations.RenameField(
            model_name='set',
            old_name='date_created',
            new_name='created',
        ),
        migrations.AddField(
            model_name='flashcard',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
