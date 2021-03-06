# pull python
FROM python:3.8

# python env
ENV PYTHONUNBUFFERED 1

# work directory
RUN mkdir /code
WORKDIR /code

# project
COPY  . /code/

# upgrade and install requirements
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# entry
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8080"]
