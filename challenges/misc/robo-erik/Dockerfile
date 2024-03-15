FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1
COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY .env .
COPY src/bot.py .
CMD export $(xargs <.env) && python3 bot.py

