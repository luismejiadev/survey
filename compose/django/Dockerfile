FROM python:3
ENV PYTHONUNBUFFERED 1
ENV APP_PROJ=/srv/survey

COPY . $APP_PROJ
RUN useradd survey && chown survey:survey -R $APP_PROJ
# RUN apt-get update && apt-get install -y supervisor

WORKDIR $APP_PROJ
RUN pip install -r requirements/base.txt
COPY compose/django/start.sh /start.sh
RUN chmod +x /start.sh && chown survey:survey /start.sh
USER survey
# COPY ./compose/django/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# CMD ["/usr/bin/supervisord"]