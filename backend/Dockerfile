FROM python:3.10-slim

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=lovelink.settings

CMD python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@gmail.com', '4152')" \
    && python manage.py collectstatic --noinput \
    && gunicorn lovelink.wsgi:application --bind 0.0.0.0:8000