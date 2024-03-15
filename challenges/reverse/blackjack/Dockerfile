FROM ubuntu

RUN apt-get update && apt-get install -y socat

WORKDIR /app
ADD blackjack flag.txt serve.sh /app/

CMD ["./serve.sh"]