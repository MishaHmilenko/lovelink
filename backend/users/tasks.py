from django.db.models import F

from lovelink.celery import app
from users.models import User


@app.task
def add_coins():
    User.objects.update(coins=F('coins') + 1)
