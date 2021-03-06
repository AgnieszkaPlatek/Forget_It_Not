# Generated by Django 3.0 on 2020-05-21 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flashcards', '0005_auto_20200104_1136'),
        ('learn', '0006_learningsession_total_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Learn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_ids', models.TextField()),
                ('total_questions', models.IntegerField(default=0)),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('set_to_learn', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flashcards.Set')),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='flashcard',
        ),
        migrations.RemoveField(
            model_name='question',
            name='session',
        ),
        migrations.DeleteModel(
            name='LearningSession',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
