
FROM python:3.8-slim

RUN PYTHONDONTWRITEBYTECODE=1
RUN PYTHONUNBUFFERED=1

WORKDIR /app


USER root


COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./core /app/

EXPOSE 8000

