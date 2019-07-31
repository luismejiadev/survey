import datetime

SURVEY_DAYS = 15
survey_end_date = lambda: datetime.date.today() + datetime.timedelta(days=SURVEY_DAYS)

def get_last_survey():
    from surveys.models import Survey
    survey = Survey.objects.all().order_by("-id")[0]
    return survey

