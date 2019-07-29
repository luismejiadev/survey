from django.db import models
import random

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class QuestionManager(models.Manager):
    def random_get(self, session_key=None, **kwargs):
        queryset = self.get_queryset().filter(**kwargs)
        if session_key is not None:
            queryset = queryset.exclude(userchoice__session_key=session_key).distinct()
        return random.choices(queryset).pop() if queryset else None

