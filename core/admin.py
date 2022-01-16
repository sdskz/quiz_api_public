from django.contrib import admin
from . import models

class AnswerInlineModel(admin.StackedInline):
    # admin.TabularInline affects on appearance inside the admin panel (built-in template)
    # need this in order to see Answers while editing Quiz
    model = models.Answer
    fields = ['answer_text']

@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'accepts_multiple_choice', 'accepts_user_custom_choice', 'date_created', 'start_date', 'expiration_date']
    inlines = [
        AnswerInlineModel
        # now we can edit all the Answers from within Quiz
    ]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer_text', 'quiz']


@admin.register(models.UserQuizResults)
class UserQuizResults(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'quiz', 'user_answer_text', 'date_created']