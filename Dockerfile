FROM python:3.8.5-slim-buster

ENV FLASK_ENV=development
ENV FLASK_APP=app

RUN apt-get update
RUN apt-get -y install sqlite

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000 5000

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]