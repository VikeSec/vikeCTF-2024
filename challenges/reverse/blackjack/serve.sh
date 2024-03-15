#!/bin/sh
socat \
-T60 \
TCP-LISTEN:12345,reuseaddr,fork \
EXEC:"./blackjack"