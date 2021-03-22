# pull base image
FROM python:3.8

# set env variable
# prevents Python from buffering stdout and stderr, output in console
ENV PYTHONUNBUFFERED 1
# creates an environment variable called DJANGO_ENV and sets it to the development environment
ENV DJANGO_ENV dev
# to load different databases depending on whether application is running inside a Docker container
ENV DOCKER_CONTAINER 1

# copies project’s requirements.txt file into a new directory in Docker called /code/
COPY ./code/requirements.txt /code/requirements.txt
# install required packages
RUN pip install -r /code/requirements.txt

# copies the rest of the code in current directory ./code into the /code/ directory
COPY ./code /code/
# set work directory 
WORKDIR /code/

# in order to access to port 8000
EXPOSE 8000
