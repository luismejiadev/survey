from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ['question_text', 'pub_date', 'is_active']
    list_filter = ['is_active']
    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'votes', 'is_active']
    list_filter = ['is_active']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)