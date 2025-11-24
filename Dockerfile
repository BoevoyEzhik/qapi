FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# set workdir
WORKDIR /app

# install dependeddcies
RUN pip install --upgrade pip
COPY ./req.txt /app/
RUN pip install -r req.txt

# copy project
COPY . /app

RUN ls -la /app
