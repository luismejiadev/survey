import logging
from celery import shared_task
from django.db.models import F
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def increment_vote(choice_id):
    from .models import Choice
    logger.info("increment {0}".format(choice_id))
    Choice.objects.filter(pk=choice_id).update(votes=F('votes')+1)
    logger.info("done")


@shared_task
def increment_counter(choice_id):
    from .utils import get_redis
    logger.info("increment {0}".format(choice_id))
    rconn = get_redis()
    rconn.incr("Choice%s" % choice_id)
    logger.info("done")
