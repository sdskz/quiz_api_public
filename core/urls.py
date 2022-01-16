from django.urls import path
from .views import QuizView, QuizViewActive, QuizChosenView

app_name = 'core'

urlpatterns = [
    path('', QuizView.as_view(), name='quizzes'),
    path('<int:quiz>/', QuizChosenView.as_view(), name='quiz-by-id'),
    path('active/', QuizViewActive.as_view(), name='quiz-active'),
]