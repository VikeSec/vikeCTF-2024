FROM debian:stable-slim

RUN apt update && apt install -y socat

COPY out/the-usual flag.txt /

RUN chmod u+x /the-usual

CMD socat TCP-LISTEN:8080,fork,reuseaddr EXEC:"/the-usual"
