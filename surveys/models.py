from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .managers import ActiveManager, QuestionManager
import datetime
from .utils import survey_end_date, get_redis


class Survey(models.Model):
    slug = models.SlugField(max_length=20)
    start_date = models.DateField(
        default=datetime.date.today,
        help_text='First day of the survey'
    )
    end_date = models.DateField(
        default=datetime.date.today,
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

    @property
    def top_questions(self):
        # TODO: improve performance with redis cache
        return sorted(self.question_set.filter(is_active=True).annotate(
            count=models.Count('userchoice')
        ), key=lambda x: -x.user_choices_count)[:10]

    def get_intertal_date(self, interval):
        if interval == 'day':
            start_date = datetime.date.today() - datetime.timedelta(days=1)
        elif interval == 'week':
            start_date = datetime.date.today() - datetime.timedelta(weeks=1)
        elif interval == 'month':
            start_date = datetime.date.today() - datetime.timedelta(weeks=4)
        else:
            start_date = datetime.date.today() - datetime.timedelta(days=365)
        return start_date

    def get_top_questions(self, interval):
        start_date = self.get_intertal_date(interval)
        query_params = {'is_active': True, 'userchoice__created_at__gte': start_date}
        return sorted(self.question_set.filter(**query_params).annotate(
            count=models.Count('userchoice')
        ), key=lambda x: -x.user_choices_count)[:10]

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=400)
    slug = models.SlugField(max_length=30)
    pub_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    objects = QuestionManager()
    active_objects = ActiveManager()

    def __str__(self):
        return "{0}: {1}".format(self.slug, self.question_text)

    @property
    def user_choices_count(self):
        return self.userchoice_set.count()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)
    active_objects = ActiveManager()

    def __str__(self):
        return "{0}: {1}".format(self.question.slug, self.choice_text)

    @property
    def stats_votes(self):
        redis_value = get_redis().get(self.redis_key) or 0
        return int(redis_value)

    @property
    def redis_key(self):
        return "Choice%s" % self.id

class UserChoice(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    # Be Careful With Cookie-Based Sessions.
    # Read Using cookie-based sessions Warning
    # https://docs.djangoproject.com/en/2.2/topics/http/sessions/
    session_key = models.CharField(max_length=32, null=True)
