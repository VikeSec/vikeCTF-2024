FROM alpine:3.18.3

RUN apk add --no-cache python3 socat

COPY challenge.py /

CMD socat TCP-LISTEN:8080,fork,reuseaddr EXEC:"python3 /challenge.py"
