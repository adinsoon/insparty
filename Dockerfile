FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./code/requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY ./code /code/
WORKDIR /code/

EXPOSE 8000
