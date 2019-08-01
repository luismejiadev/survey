import datetime
from django.test import TestCase
from surveys.managers import QuestionManager
from surveys.models import Question, Survey

class QuestionManagerTestCase(TestCase):
    def setUp(self):
        now =  datetime.datetime.now()
        self.survey = Survey.objects.create(slug='2019')
        Question.objects.create(
            question_text="how are you?",
            pub_date=now,
            survey=self.survey)

    def test_random_get_with_empty_active_queryset(self):
        Question.objects.all().update(is_active=False)
        question = Question.objects.random_get()
        self.assertIsNone(question)

    def test_random_get_without_session_key(self):
        question = Question.objects.random_get()
        self.assertIsNotNone(question)

    def test_random_get_with_session_key_with_choices(self):
        question = Question.objects.random_get('test')
        self.assertIsNotNone(question)

    def test_random_get_with_session_key_no_choices(self):
        question = Question.objects.all()[0]
        question.choice_set.create(choice_text='ok', id=1)
        question.userchoice_set.create(session_key='test', choice_id=1)
        question = Question.objects.random_get('test')
        self.assertIsNone(question)
