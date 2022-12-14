# pull official base image
FROM python:3.10.0-alpine

# set work directory
# create the appropriate directories
ENV HOME=/home/ubuntu/cogncise/
ENV APP_HOME=/home/ubuntu/cogncise/crm_backend
WORKDIR $APP_HOME

RUN mkdir staticfiles
RUN mkdir mediafiles



# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# copy project
# copy project
COPY . $APP_HOME