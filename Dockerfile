FROM python:3.8


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code/
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 8000