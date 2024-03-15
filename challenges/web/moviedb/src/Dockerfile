FROM python

WORKDIR /app

ADD --chmod=644 requirements.txt /app
RUN python -m pip install -r requirements.txt

ADD --chmod=644 server.py index.html movies.sqlite3 /app/
ADD --chmod=644 static/ /app/static/

RUN useradd -M worker

EXPOSE 8000

ADD --chmod=700 healthcheck.sh /app
HEALTHCHECK --interval=1s --timeout=1s --start-period=5s --retries=5 CMD [ "/app/healthcheck.sh" ]

CMD [ "gunicorn", "server:app", \
    "--worker-class=gevent", "--bind=0.0.0.0:8000", "--user=worker" \
    ]