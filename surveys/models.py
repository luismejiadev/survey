from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .managers import ActiveManager, QuestionManager
import datetime
from .utils import survey_end_date


class Survey(models.Model):
    slug = models.SlugField(max_length=20)
    start_date = models.DateField(
        default=datetime.date.today,
        help_text='First day of the survey'
    )
    end_date = models.DateField(
        default=survey_end_date,
        help_text='Last day of the survey'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('survey_detail', args=[self.slug])

    @property
    def questions_count(self):
        return self.question_set.count()

    @property
    def active_questions_count(self):
        return self.question_set.filter(is_active=True).count()

    @property
    def user_choices_count(self):
        return self.question_set.filter(userchoice__isnull=False).count()

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=400)
    slug = models.SlugField(max_length=30)
    pub_date = models.DateTimeField(default=survey_end_date)
    is_active = models.BooleanField(default=True)

    objects = QuestionManager()
    active_objects = ActiveManager()

    def __str__(self):
        return "{0}: {1}".format(self.slug, self.question_text)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)
    active_objects = ActiveManager()

    def __str__(self):
        return "{0}: {1}".format(self.question.slug, self.choice_text)

class UserChoice(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    # Be Careful With Cookie-Based Sessions.
    # Read Using cookie-based sessions Warning
    # https://docs.djangoproject.com/en/2.2/topics/http/sessions/
    session_key = models.CharField(max_length=32, null=True)
