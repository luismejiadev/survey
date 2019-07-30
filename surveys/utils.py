import datetime

SURVEY_DAYS = 15
survey_end_date = lambda: datetime.date.today() + datetime.timedelta(days=SURVEY_DAYS)

