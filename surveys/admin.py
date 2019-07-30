from django.contrib import admin
from .models import Question, Choice, UserChoice, Survey
from django.contrib import messages as flash_messages

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ['question_text', 'pub_date', 'is_active']
    list_filter = ['survey', 'is_active']
    inlines = [ChoiceInline]
    actions = ['active_questions', 'deactive_questions']

    def active_questions(self, request, queryset):
        count = queryset.filter(is_active=False).update(is_active=True)
        message = "{0} questions activated".format(count)
        # Read Message Framework
        # https://docs.djangoproject.com/en/2.2/ref/contrib/messages/#adding-a-message
        flash_messages.success(request, message)

    def deactive_questions(self, request, queryset):
        count = queryset.filter(is_active=True).update(is_active=False)
        message = "{0} questions deactivated".format(count)
        # Read Message Framework
        # https://docs.djangoproject.com/en/2.2/ref/contrib/messages/#adding-a-message
        flash_messages.error(request, message)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'votes', 'is_active']
    list_filter = ['is_active']

class UserChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice', 'session_key']
    readonly_fields = ['question', 'choice', 'session_key', 'user']

    def get_actions(self, request):
        return []

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['slug', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active']
    inlines = [QuestionInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(UserChoice, UserChoiceAdmin)
admin.site.register(Survey, SurveyAdmin)

