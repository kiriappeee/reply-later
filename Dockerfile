FROM python:3.5

RUN apt-get update && apt-get install -y cron vim
RUN pip install Flask twitter-text-python tweepy python-crontab requests
ADD . /app
WORKDIR /app
EXPOSE 5000

CMD cron && python serverstart.py
