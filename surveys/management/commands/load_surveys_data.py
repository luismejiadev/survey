import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core.management.commands.loaddata import Command as LoadDataCommand
from django.conf import settings
from django.db import connection

from surveys.models import Question, Survey, Choice, UserChoice

class Command(BaseCommand):
    help = 'Load data for surveys, choices and Userchoices in fixture'

    def success_msg(self, question_code):
        msg = 'Data soaded successfully'
        self.stdout.write(self.style.SUCCESS(msg))

    def handle(self, *args, **options):
        # Read Running management commands from your code
        # https://docs.djangoproject.com/en/2.2/ref/django-admin/#running-management-commands-from-your-code
        call_command(LoadDataCommand(), 'surveys')
        call_command(LoadDataCommand(), 'questions')
        self.load_user_choices()
        Question.objects.filter(choice__isnull=True).update(is_active=False)

    def load_questions(self):
        dir_path = os.path.join(settings.BASE_DIR, 'surveys', 'fixtures', 'data')
        df = pd.read_csv(dir_path + '/questions.zip')
        for index, row in df.iterrows():
            Question.objects.get_or_create(slug=row[0], question_text=row[1], survey_id=1)

    def load_user_choices(self):
        dir_path = os.path.join(settings.BASE_DIR, 'surveys', 'fixtures', 'data')
        df = pd.read_csv(dir_path + '/user_choices.zip')
        for column in df:
            print("Importing Choices for {0}".format(column))
            question = Question.objects.get(slug=str(column))
            for choice_value in df[column].dropna().unique():
                print(choice_value)
                choice, created = question.choice_set.get_or_create(choice_text=choice_value)
                UserChoice.objects.get_or_create(question=question, choice=choice)
