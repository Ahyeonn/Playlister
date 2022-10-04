FROM python:3.7-slim-buster

ADD . /app

WORKDIR /app


ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"]
