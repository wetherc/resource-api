FROM python:3.9-slim

ENV PYTHONBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

RUN pip install flask gunicorn kubernetes

CMD exec gunicorn --bind $PORT --workers 1 --threads 1 --timeout 0 main:app
