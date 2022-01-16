from rest_framework.response import Response
from .models import Quiz, Answer, UserQuizResults
from .serializers import QuizSerializer, AnswerSerializer, UserQuizResultsSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone as django_timezone
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class QuizView(APIView):
    # path /quiz/
    @swagger_auto_schema(
        operation_description="Получение всех Quiz из бд. Никакой сортировки нет\n"
                              "Пользователь может выбрать Quiz по id и затем ответить на него через post запрос, используя в url выбранный id в качестве идентификатора",
        operation_summary='Get all the Quizzes (active and not active)',
    )
    def get(self, request, **kwargs):
        queryset = Quiz.objects.all()
        serializer_object = QuizSerializer(queryset, many=True)
        return Response(serializer_object.data, status=status.HTTP_200_OK)

class QuizChosenView(APIView):
    # path /quiz/<int:quiz>/
    @swagger_auto_schema(
        operation_description="Получение определенного Quiz через его id в url\n"
                              "id должен быть integer (никак не валидируется)\n"
                              "Если id указать чем-либо кроме целого числа, будет 404\n"
                              "Если указать id правильно (целым числом), но в бд нет такого Quiz, то ошибка обработается, вернется 400 и ответ в json"
                              "Пользователь может выбрать Quiz по id и затем ответить на него через post запрос, используя в url выбранный id в качестве идентификатора\n",
        operation_summary='Get a particular Quiz by its id',
    )
    def get(self, request, **kwargs):
        queryset = Quiz.objects.filter(id=kwargs['quiz'])
        serializer_object = QuizSerializer(queryset, many=True)
        if queryset.exists():
            return Response(serializer_object.data, status=status.HTTP_200_OK)
        else:
            return Response({"response": f'Quiz with id {kwargs["quiz"]} does not exist!'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Пользователь отвечает серверу на Quiz, идентификатор Quiz включен в url\n"
                              "user_id - нужно указать уникальный (один юзер два раза не может участвовать в опросе, иначе придет 400)\n"
                              "quiz - текущий квиз, на который дается ответ (если пользователь решит вставить другой id квиза, то система автоматически подставит id, который пользователь указал в url)\n"
                              "user_answer_text - можно указывать любой из suggested_answers в этом квизе (или вставить свой кастомный ответ)\n"
                              "user_answer_text - проходит валидацию (если кастомные ответы не разрешены, система ответит 400)\n",
        operation_summary='Post an Answer to a chosen Quiz',
        request_body=UserQuizResultsSerializer,
    )
    def post(self, request, **kwargs):
        quiz_check = kwargs["quiz"] # got quiz_id from the url
        request.data["quiz"] = quiz_check # serializer needs to know, which quiz_id to work with
        serializer_object = UserQuizResultsSerializer(data=request.data)
        # if user tries to cheat and provides wrong quiz_id, we will get anyway quiz_id from the url
        if serializer_object.is_valid():
            user_check = request.data["user_id"]
            check_user_participation = UserQuizResults.objects.filter(user_id=int(user_check), quiz=int(quiz_check))
            if not check_user_participation.exists():
                # (y/n) if user did participate in any Quiz
                is_custom_choice = Quiz.objects.get(id=int(quiz_check)).accepts_user_custom_choice
                if is_custom_choice:
                    # if Quiz accepts answer not in the suggested list
                    serializer_object.save()
                    return Response(serializer_object.data, status=status.HTTP_201_CREATED)
                if not is_custom_choice:
                    # user can only input value from the suggested_values
                    user_answer_text = request.data["user_answer_text"]
                    check_user_answer_text = Quiz.objects.get(id=int(quiz_check)).\
                        suggested_answers.values_list('answer_text').\
                        filter(answer_text=user_answer_text)
                    if check_user_answer_text.exists():
                        # checks if user_answer_text in the suggested_values
                        serializer_object.save()
                        return Response(serializer_object.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"response": f"User id ({user_check}), sends custom answer ({user_answer_text}) "
                                                     f"=> this Quiz only accepts suggested_answers!"},
                                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response": f'User id {user_check}, Quiz id {quiz_check} '
                                             f'=> user_already_participated_in_this_question'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_object.errors, status=status.HTTP_400_BAD_REQUEST)



class QuizViewActive(APIView):
    # path /quiz/active/
    @swagger_auto_schema(
        operation_description="Отсортированные Quiz из бд, активные на текущее время\n"
                              "Пользователь может выбрать Quiz по id и затем ответить на него через post запрос, используя в url выбранный id в качестве идентификатора",
        operation_summary='Get all the Quizzes (active)',
    )
    def get(self, request, **kwargs):
        # all the active questions for now
        now = django_timezone.now()
        queryset = Quiz.objects.filter(expiration_date__gt=now) # > greater than now time
        serializer_object = QuizSerializer(queryset, many=True)
        if queryset.exists():
            # queryset not empty => there are some active questions
            return Response(serializer_object.data, status=status.HTTP_200_OK)
        else:
            return Response({"response": "by today, there is no active Quizzes, try next time"}, status=status.HTTP_400_BAD_REQUEST)

class AnswerView(APIView):
    # path /answers/<int:user_id>/
    # user_id defines which user's Answers to show
    @swagger_auto_schema(
        operation_description="Получение всех ответов пользователя, используя id пользователя\n"
                              "Получаемый id должен быть всегда integer (id никак не валидируется)\n"
                              "Будет ответ 404 если указать не число, 400 если указано число, но пользователь с таким id не найден в бд",
        operation_summary='Get all the Answers by user_id',
    )
    def get(self, request, **kwargs):
        user_check = kwargs['user_id']
        print(request.data)
        queryset = UserQuizResults.objects.filter(user_id=user_check)
        serializer_object = UserQuizResultsSerializer(queryset, many=True)
        if queryset.exists():
            # queryset not empty => hence this user did answer some Questions
            return Response(serializer_object.data, status=status.HTTP_200_OK)
        else:
            return Response({"response": f'User id {user_check} => did_not_answered_any_questions OR does_not_exist'}, status=status.HTTP_400_BAD_REQUEST)