from django.db import models

class Created(models.Model):
    date_created = models.DateTimeField(verbose_name="Created", auto_now=True)
    # auto_now=True adds current time when updated
    class Meta:
        # abstract models do not have its table in the db
        # can be used as a parent model to eliminate creating duplicate field in all the child models
        # when inherited, provide to a child model its own field
        abstract = True


class Quiz(Created):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.CharField(max_length=255, verbose_name="Description", null=True, blank=True)
    accepts_multiple_choice = models.BooleanField(default=False, verbose_name="Is User Multiple Choice Available")
    accepts_user_custom_choice = models.BooleanField(default=True, verbose_name="Is User Custom Choice Available")
    start_date = models.DateTimeField(verbose_name="Start Date", auto_now=True)
    # start_date cannot be changed in the admin panel
    # by default, start_date == date_created
    expiration_date = models.DateTimeField(verbose_name="Expiration Date", null=True, blank=True)
    # expiration_date is at admin's discretion. may vary

    class Meta:
        # adjusting appearance inside admin panel
        ordering = ["id"]
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quiz'


    def __str__(self):
        return self.title


class Answer(Created):
    quiz = models.ForeignKey(Quiz, related_name='suggested_answers', on_delete=models.DO_NOTHING)
    # each Question may be represented by many suggested answers
    # if Answer deleted, Question must not
    # related_name='answer' enables us to access from within the other model (using __ double underscore)
    answer_text = models.CharField(max_length=255, verbose_name="Answer Text")

    class Meta:
        ordering = ["id"]
        verbose_name = 'Answer'
        verbose_name_plural = 'Answer'

    def __str__(self):
        return self.answer_text


class UserQuizResults(Created):
    user_id = models.IntegerField()
    quiz = models.ForeignKey(Quiz, related_name='quiz', on_delete=models.DO_NOTHING)
    user_answer_text = models.TextField(max_length=255)

    class Meta:
        ordering = ["id"]
        verbose_name = 'UserQuizResults'
        verbose_name_plural = 'UserQuizResults'

    def __str__(self):
        return self.user_answer_text
