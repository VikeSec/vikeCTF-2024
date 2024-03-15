FROM alpine:3.19.1

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt .

RUN pip install --break-system-packages -r requirements.txt

COPY flag.html login.html server.py .

CMD python3 server.py
