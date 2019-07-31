import json
import logging
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import UserChoice, Question, Survey
from .tasks import increment_vote

logger = logging.getLogger(__name__)


class RandomQuestionMixin(object):

    @property
    def current_session_key(self):
        if not self.request.session.session_key:
            self.request.session.save()
        session_key = self.request.session.session_key
        return session_key

    def get_random_question(self):
        return Question.objects.random_get(self.current_session_key)

    def get_current_progress(self):
        questions_count = Question.objects.filter(is_active=True).count()
        user_choices = UserChoice.objects.filter(question__is_active=True)
        user_choices_count = user_choices.filter(**self.session_param()).count()
        return (user_choices_count * 100 // questions_count) if questions_count > 0 else 100

    def session_param(self):
        if self.request.user.is_authenticated:
            query_params = {'user': self.request.user}
        else:
            query_params = {'session_key': self.current_session_key}
        return query_params


class IndexView(RandomQuestionMixin, TemplateView):
    template_name = 'surveys/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add extra context
        question = self.get_random_question()
        if question is not None:
            context.update({'questions': [question]})
        context['current_progress'] = self.get_current_progress()
        return context


class UserChoiceCreateView(RandomQuestionMixin, CreateView):
    model = UserChoice
    fields = ['question', 'choice']

    def get_success_url(self):
        return reverse('index')

    def form_invalid(self, form):
        responsedict = {
            'errors': form.errors,
            'status': False
        }
        return HttpResponse(json.dumps(responsedict))

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.session_key = self.current_session_key
        form.save()
        increment_vote.delay(form.instance.choice_id)
        messages.success(self.request, 'Your choice was save successfully.')
        return super().form_valid(form)

def start_again(request):
    request.session.flush()
    messages.success(request, "Let's do it again")
    return redirect('index')


class SurveyListView(LoginRequiredMixin, ListView):
    model = Survey
    paginate_by = 10


class SurveyDetailView(LoginRequiredMixin, DetailView):
    model = Survey


def questions_view(request, slug):
    interval = request.GET.get('interval', 'year')
    labels = []
    data = []
    try:
        obj = Survey.objects.get(slug=slug)
        for question in obj.get_top_questions(interval):
            labels.append(question.slug)
            data.append(question.user_choices_count)
        responsedict = {
            'data': data,
            'labels': labels
        }
    except Survey.DoesNotExist:
        pass

    responsedict = {
        'data': data,
        'labels': labels
    }
    return HttpResponse(json.dumps(responsedict))
