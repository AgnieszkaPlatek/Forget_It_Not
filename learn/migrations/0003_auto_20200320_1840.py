# Generated by Django 3.0 on 2020-03-20 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_auto_20200320_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learningsession',
            name='questions_count',
        ),
        migrations.RemoveField(
            model_name='learningsession',
            name='total_questions',
        ),
    ]
