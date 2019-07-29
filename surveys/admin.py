from django.contrib import admin
from .models import Question, Choice
from django.contrib import messages as flash_messages

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ['question_text', 'pub_date', 'is_active']
    list_filter = ['is_active']
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

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)