FROM python:3.5

RUN pip install Flask twitter-text-python tweepy crontab requests
ADD . /app
WORKDIR /app
EXPOSE 5000
CMD python serverstart.py
