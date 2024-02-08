from celery import shared_task
from django.db.models import F
import logging

from lovelink.celery import app
from users.models import User


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.task
def add_coins():
    logger.info('Start task')
    try:
        User.objects.update(coins=F('coins') + 1)
        logger.info('Finish task')
    except Exception as e:
        logger.error(f'An error occurred: {e}')
