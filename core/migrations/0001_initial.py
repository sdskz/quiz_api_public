# Generated by Django 2.2.10 on 2022-01-16 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Created time')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('accepts_multiple_choice', models.BooleanField(default=False, verbose_name='Is User Multiple Choice Available')),
                ('accepts_user_custom_choice', models.BooleanField(default=True, verbose_name='Is User Custom Choice Available')),
                ('start_date', models.DateTimeField(auto_now=True, verbose_name='Start Date')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Expiration Date')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quiz',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserQuizResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Created time')),
                ('user_id', models.IntegerField()),
                ('user_answer_text', models.CharField(max_length=255)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='quiz', to='core.Quiz')),
            ],
            options={
                'verbose_name': 'UserQuizResults',
                'verbose_name_plural': 'UserQuizResults',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Created time')),
                ('answer_text', models.CharField(max_length=255, verbose_name='Answer Text')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='answer', to='core.Quiz')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answer',
                'ordering': ['id'],
            },
        ),
    ]
