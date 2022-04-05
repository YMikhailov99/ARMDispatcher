# установка базового образа (host OS)
FROM python:3.8


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# установка рабочей директории в контейнере
WORKDIR /code

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .

# установка зависимостей
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --dev
RUN pip install -r requirements.txt


COPY . /code/

# команда, выполняемая при запуске контейнера
#CMD [ "python", "./app/main.py" ]
EXPOSE 8000
#CMD [ "python", "./app/main.py" ]