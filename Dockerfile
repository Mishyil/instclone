FROM python:3.10-alpine


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt .
RUN apk add  gcc libc-dev linux-headers
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


COPY app /app
WORKDIR /app

RUN adduser --disabled-password instclone-user
USER instclone-user

