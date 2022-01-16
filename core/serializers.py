from rest_framework import serializers
from .models import Quiz, Answer, UserQuizResults


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'quiz', 'answer_text']

class QuizSerializer(serializers.ModelSerializer):
    suggested_answers = AnswerSerializer(many=True, read_only=True)
    # Answer must have related_name='suggested_answers'
    class Meta:
        model = Quiz # model we want to use
        # fields = '__all__' # data we want to collect and then push that over the front-end
        fields = [
            'id',
            'title',
            'description',
            'accepts_multiple_choice',
            'accepts_user_custom_choice',
            'start_date',
            'expiration_date',
            'suggested_answers'
        ]

class UserQuizResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizResults
        fields = ['user_id', 'quiz', 'user_answer_text']
