FROM python:3.7-slim-buster

RUN mkdir app

RUN pip install -U pip setuptools wheel

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir app/auto_vlog
COPY translator_ui/ /app/translator_ui/

EXPOSE 9090

RUN mkdir /app/data/
WORKDIR /app/translator_ui


CMD [ "python", "app.py" ]