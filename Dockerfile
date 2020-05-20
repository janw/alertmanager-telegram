FROM python:3.8-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./alertmanager_telegram /alertmanager_telegram
COPY ./templates /templates

EXPOSE 8080
VOLUME [ "/templates" ]
ENTRYPOINT [ "gunicorn", "alertmanager_telegram.wsgi:app", "--logger-class", "alertmanager_telegram.logging.GunicornLogger", "-b", "0.0.0.0:8080" ]
