from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20)
    pub_date = models.DateTimeField('date published')
    is_active = models.BooleanField(default=True)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)

class UserChoice(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    # Be Careful With Cookie-Based Sessions.
    # Read Using cookie-based sessions Warning
    # https://docs.djangoproject.com/en/2.2/topics/http/sessions/
    session_key = models.CharField(max_length=32, null=True)
