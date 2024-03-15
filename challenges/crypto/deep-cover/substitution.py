cipher = {
    "a": "y",
    "b": "p",
    "c": "m",
    "d": "n",
    "e": "f",
    "f": "g",
    "g": "o",
    "h": "r",
    "i": "b",
    "j": "i",
    "k": "u",
    "l": "l",
    "m": "s",
    "n": "a",
    "o": "k",
    "p": "t",
    "q": "j",
    "r": "z",
    "s": "q",
    "t": "h",
    "u": "d",
    "v": "c",
    "w": "v",
    "x": "e",
    "y": "x",
    "z": "w",
}


def translate(c):
    if str.isupper(c):
        upper = True
        c = str.lower(c)
    else:
        upper = False

    if c in cipher:
        c = cipher[c]

    if upper:
        c = str.upper(c)

    return c


with open("plaintext.txt", "r") as f:
    plaintext = f.read()


ciphertext = "".join([translate(c) for c in plaintext])

with open("ciphertext.txt", "w") as f:
    f.write(ciphertext)
